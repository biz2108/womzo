# Copyright (C) 2026 SJB
# SPDX-License-Identifier: AGPL-3.0-only

"""Functional tests for an isolated World Webcams installation."""

import json
import re
import sys
import http.cookiejar
from pathlib import Path
from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from urllib.error import HTTPError

BASE = "http://127.0.0.1:18099"

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 tests/test_http.py TEST_ENV_FILE")

config = dict(
    line.split("=", 1)
    for line in Path(sys.argv[1]).read_text().splitlines()
    if "=" in line and not line.lstrip().startswith("#")
)

version = (
    Path(__file__).resolve().parent.parent / "VERSION"
).read_text().strip()

browser = build_opener(
    HTTPCookieProcessor(http.cookiejar.CookieJar())
)

def request(path, data=None):
    payload = urlencode(data).encode() if data is not None else None
    try:
        with browser.open(BASE + path, payload, timeout=10) as r:
            return r.status, r.read().decode(), r.geturl()
    except HTTPError as e:
        return e.code, e.read().decode(), e.geturl()

def check(condition, description):
    if not condition:
        raise AssertionError("FAIL: " + description)
    print("PASS:", description)

def csrf(html):
    return re.search(
        r'name="csrf_token" value="([^"]+)"', html
    ).group(1)

def cameras():
    status, html, _ = request("/")
    assert status == 200
    return json.loads(re.search(
        r'<script id="camera-data" type="application/json">(.*?)</script>',
        html, re.S
    ).group(1))

status, body, _ = request("/healthz")
check(status == 200 and json.loads(body)["status"] == "ok",
      "Application health endpoint")

status, html, _ = request("/")
check(status == 200 and cameras() == [],
      "Fresh installation has an empty camera collection")

check(f"v{version}" in html, "Correct application version")

check(
    f"https://github.com/biz2108/sjb-world-webcams/tree/v{version}" in html,
    "Version-specific GitHub source link"
)

check("Webcam permissions and privacy" in html,
      "New About section")

status, html, url = request("/admin")
check(url.endswith("/admin/login"),
      "Unauthenticated administration blocked")

status, _, _ = request("/admin/login", {
    "password": config["ADMIN_PASSWORD"]
})
check(status == 400, "Login without CSRF token rejected")

_, html, _ = request("/admin/login")

status, html, url = request("/admin/login", {
    "password": config["ADMIN_PASSWORD"],
    "csrf_token": csrf(html)
})
check(status == 200 and url.endswith("/admin"),
      "Administrator login")

token = csrf(html)

for title in ("Test Camera A", "Test Camera B"):
    status, _, _ = request("/admin/add", {
        "csrf_token": token,
        "title": title,
        "location": "Test location",
        "url": "https://example.invalid/camera.jpg"
    })
    assert status == 200

items = cameras()
check(len(items) == 2, "Add two cameras")

a, b = items[0]["id"], items[1]["id"]

request(f"/admin/edit/{a}", {
    "csrf_token": token,
    "title": "Edited Camera A",
    "location": "Test location",
    "url": "https://example.invalid/edited.jpg"
})

check(cameras()[0]["title"] == "Edited Camera A",
      "Edit camera")

request(f"/admin/move/{b}/up", {
    "csrf_token": token
})

check(cameras()[0]["id"] == b,
      "Reorder cameras")

status, _, _ = request(f"/admin/delete/{a}", {
    "csrf_token": "invalid"
})
check(status == 400 and len(cameras()) == 2,
      "Invalid deletion token rejected")

for camera_id in (a, b):
    request(f"/admin/delete/{camera_id}", {
        "csrf_token": token
    })

check(cameras() == [], "Delete cameras")

request("/admin/logout", {"csrf_token": token})

_, _, url = request("/admin")
check(url.endswith("/admin/login"),
      "Logout and administrator access revoked")

print("\nALL 14 FUNCTIONAL TESTS PASSED")
