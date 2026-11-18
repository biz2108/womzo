# Copyright (C) 2026 SJB
# SPDX-License-Identifier: AGPL-3.0-only
# See LICENSE for the full licence terms.

"""A small, read-only public webcam directory with a password-protected admin page.

Video is fetched by viewers' browsers directly from upstream providers. This server
only stores and serves bookmarks and never proxies user-provided URLs.
"""
import hmac
import os
import re
import secrets
import sqlite3
import time
import math
from functools import wraps
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

DB_PATH = Path(os.environ.get("DB_PATH", "/data/webcams.sqlite3"))
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not ADMIN_PASSWORD or ADMIN_PASSWORD.startswith("replace_") or len(ADMIN_PASSWORD) < 16:
    raise RuntimeError("Set an ADMIN_PASSWORD of at least 16 characters in .env")
if not SECRET_KEY or SECRET_KEY.startswith("replace_") or len(SECRET_KEY) < 32:
    raise RuntimeError("Set a SECRET_KEY of at least 32 characters in .env")

app = Flask(__name__)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_NAME="worldcams_session",
    SESSION_COOKIE_SECURE=os.environ.get(
        "SESSION_COOKIE_SECURE", "true"
    ).lower() == "true",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=8 * 60 * 60,
    MAX_CONTENT_LENGTH=32 * 1024,
)

YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def connection():
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connection() as con:
        # Gunicorn starts multiple workers: serialise schema migration across them.
        con.execute("BEGIN IMMEDIATE")
        con.execute("""
            CREATE TABLE IF NOT EXISTS admin_login_failures (
                attempted_at REAL NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS cameras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                url TEXT NOT NULL,
                kind TEXT NOT NULL,
                youtube_id TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                sort_order INTEGER
            )
        """)
        columns = {row["name"] for row in con.execute("PRAGMA table_info(cameras)")}
        if "sort_order" not in columns:
            con.execute("ALTER TABLE cameras ADD COLUMN sort_order INTEGER")
            # Preserve the familiar alphabetical order on the first upgrade.
            original = con.execute("""
                SELECT id FROM cameras
                ORDER BY location COLLATE NOCASE, title COLLATE NOCASE, id
            """).fetchall()
            for position, row in enumerate(original, start=1):
                con.execute("UPDATE cameras SET sort_order = ? WHERE id = ?", (position, row["id"]))


init_db()



def classify_url(raw_url):
    url = raw_url.strip()

    if not url or len(url) > 2048:
        raise ValueError(
            "Enter a webcam URL (maximum 2048 characters)."
        )

    # Reject control characters and backslashes.
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in url) or "\\" in url:
        raise ValueError("URL contains invalid characters.")

    parts = urlsplit(url)

    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username
        or parts.password
    ):
        raise ValueError(
            "Use an HTTPS webcam URL without embedded credentials."
        )

    # Reject invalid port numbers.
    try:
        _ = parts.port
    except ValueError as exc:
        raise ValueError("Invalid port in webcam URL.") from exc

    host = parts.hostname.lower()
    path = parts.path
    youtube_id = None

    # YouTube URLs.
    if host in {"youtu.be", "www.youtu.be"}:
        youtube_id = path.strip("/").split("/")[0]

    elif host in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtube-nocookie.com",
        "www.youtube-nocookie.com",
    }:
        if path == "/watch":
            youtube_id = parse_qs(parts.query).get("v", [""])[0]

        elif path.startswith(("/live/", "/embed/", "/shorts/")):
            segments = path.strip("/").split("/")

            if len(segments) >= 2:
                youtube_id = segments[1]

    if youtube_id and YOUTUBE_ID_RE.fullmatch(youtube_id):
        return url, "youtube", youtube_id

    # IPCamLive public iframe player.
    if (
        re.fullmatch(r"g[0-9]+\.ipcamlive\.com", host)
        and path == "/player/player.php"
    ):
        aliases = parse_qs(parts.query).get("alias", [])

        if (
            len(aliases) == 1
            and re.fullmatch(r"[A-Za-z0-9_-]{1,80}", aliases[0])
        ):
            return url, "ipcamlive", None

    # MyEarthCam embed player.
    if host in {"www.myearthcam.com", "myearthcam.com"}:
        params = parse_qs(parts.query, keep_blank_values=True)

        if (
            re.fullmatch(r"/[A-Za-z0-9_-]{1,80}/?", path)
            and "embed" in params
        ):
            return url, "myearthcam", None

    # HLS streams.
    if path.lower().endswith(".m3u8"):
        return url, "hls", None

    # Camera images.
    if path.lower().endswith(
        (".jpg", ".jpeg", ".png", ".mjpg", ".mjpeg")
    ):
        return url, "image", None

    # Other HTTPS websites open at their original source.
    return url, "link", None



def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token
app.jinja_env.globals["app_version"] = (
    Path(__file__).with_name("VERSION").read_text().strip()
)


def require_csrf():
    expected = session.get("csrf_token", "")
    submitted = request.form.get("csrf_token", "")
    if not expected or not hmac.compare_digest(
        expected.encode("utf-8"),
        submitted.encode("utf-8")
    ):
        abort(400, "Invalid form token; refresh the page and retry.")


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper


def camera_list():
    with connection() as con:
        rows = con.execute("SELECT * FROM cameras ORDER BY sort_order ASC, id ASC").fetchall()
        return [dict(row) for row in rows]



@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    if request.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-store"

    # Test the Content Security Policy without blocking resources.
    csp = [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self'",
        "img-src 'self' https: data:",
        "media-src 'self' https: blob:",
        "connect-src 'self' https:",
        "worker-src 'self' blob:",
        "frame-src https://www.youtube-nocookie.com "
        "https://*.ipcamlive.com "
        "https://myearthcam.com "
        "https://www.myearthcam.com",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
    ]

    response.headers["Content-Security-Policy"] = "; ".join(csp)

    return response



@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return render_template("index.html", cameras=camera_list())

def check_admin_password(supplied):
    max_attempts = 5
    window = 60

    with connection() as con:
        con.execute("BEGIN IMMEDIATE")
        now = time.time()

        con.execute(
            "DELETE FROM admin_login_failures WHERE attempted_at <= ?",
            (now - window,)
        )

        row = con.execute("""
            SELECT COUNT(*) AS failures,
                   MIN(attempted_at) AS oldest
            FROM admin_login_failures
        """).fetchone()

        if row["failures"] >= max_attempts:
            retry_after = max(
                1, math.ceil(row["oldest"] + window - now)
            )
            return False, retry_after

        if hmac.compare_digest(
            supplied.encode("utf-8"),
            ADMIN_PASSWORD.encode("utf-8")
        ):
            con.execute("DELETE FROM admin_login_failures")
            return True, 0

        con.execute(
            "INSERT INTO admin_login_failures (attempted_at) VALUES (?)",
            (now,)
        )

    app.logger.warning("Failed administrator login attempt")
    return False, 0


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        require_csrf()
        supplied = request.form.get("password", "")

        authenticated, retry_after = check_admin_password(supplied)

        if retry_after:
            return render_template(
                "login.html",
                retry_after=retry_after
            ), 429, {
                "Retry-After": str(retry_after)
            }

        if authenticated:
            session.clear()
            session["admin"] = True
            csrf_token()
            return redirect(url_for("admin"))

        flash("Incorrect password.", "error")

    return render_template("login.html")


@app.post("/admin/logout")
@login_required
def logout():
    require_csrf()
    session.clear()
    return redirect(url_for("index"))


@app.get("/admin")
@login_required
def admin():
    return render_template("admin.html", cameras=camera_list())


def get_camera_or_404(camera_id):
    with connection() as con:
        item = con.execute("SELECT * FROM cameras WHERE id = ?", (camera_id,)).fetchone()
    if item is None:
        abort(404)
    return dict(item)


def fields_from_form():
    title = request.form.get("title", "").strip()
    location = request.form.get("location", "").strip()
    if not title or len(title) > 100:
        raise ValueError("Enter a title (maximum 100 characters).")
    if not location or len(location) > 80:
        raise ValueError("Enter a location or category (maximum 80 characters).")
    url, kind, youtube_id = classify_url(request.form.get("url", ""))
    return title, location, url, kind, youtube_id


@app.post("/admin/add")
@login_required
def add_camera():
    require_csrf()
    try:
        fields = fields_from_form()
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("admin"))
    with connection() as con:
        con.execute("BEGIN IMMEDIATE")
        next_order = con.execute(
            "SELECT COALESCE(MAX(sort_order), 0) + 1 FROM cameras"
        ).fetchone()[0]
        con.execute("""
            INSERT INTO cameras (title, location, url, kind, youtube_id, sort_order)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (*fields, next_order))
    flash("Camera added.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/edit/<int:camera_id>", methods=["GET", "POST"])
@login_required
def edit_camera(camera_id):
    camera = get_camera_or_404(camera_id)
    if request.method == "POST":
        require_csrf()
        try:
            fields = fields_from_form()
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("edit_camera", camera_id=camera_id))
        with connection() as con:
            con.execute("UPDATE cameras SET title=?, location=?, url=?, kind=?, youtube_id=? WHERE id=?", (*fields, camera_id))
        flash("Camera updated.", "success")
        return redirect(url_for("admin"))
    return render_template("edit.html", camera=camera)


@app.post("/admin/delete/<int:camera_id>")
@login_required
def delete_camera(camera_id):
    require_csrf()
    get_camera_or_404(camera_id)
    with connection() as con:
        con.execute("DELETE FROM cameras WHERE id = ?", (camera_id,))
    flash("Camera removed.", "success")
    return redirect(url_for("admin"))


@app.post("/admin/move/<int:camera_id>/<direction>")
@login_required
def move_camera(camera_id, direction):
    require_csrf()
    if direction not in {"up", "down"}:
        abort(404)
    with connection() as con:
        con.execute("BEGIN IMMEDIATE")
        rows = con.execute(
            "SELECT id, sort_order FROM cameras ORDER BY sort_order ASC, id ASC"
        ).fetchall()
        position = next((idx for idx, row in enumerate(rows) if row["id"] == camera_id), None)
        if position is None:
            abort(404)
        other_position = position + (-1 if direction == "up" else 1)
        if 0 <= other_position < len(rows):
            current = rows[position]
            neighbour = rows[other_position]
            con.execute(
                "UPDATE cameras SET sort_order = ? WHERE id = ?",
                (neighbour["sort_order"], current["id"]),
            )
            con.execute(
                "UPDATE cameras SET sort_order = ? WHERE id = ?",
                (current["sort_order"], neighbour["id"]),
            )
    return redirect(url_for("admin", _anchor=f"camera-{camera_id}"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
