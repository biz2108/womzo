# Copyright (C) 2026 SJB
# SPDX-License-Identifier: AGPL-3.0-only

"""Security configuration tests for World Webcams."""

import os
import subprocess
import sys
import tempfile

cases = [
    (None, True),
    ("true", True),
    ("false", False),
    ("ture", None),
    ("invalid", None),
]

with tempfile.TemporaryDirectory() as tmp:
    for value, expected in cases:
        env = os.environ.copy()
        env["DB_PATH"] = tmp + "/test.sqlite3"

        if value is None:
            env.pop("SESSION_COOKIE_SECURE", None)
        else:
            env["SESSION_COOKIE_SECURE"] = value

        result = subprocess.run(
            [sys.executable, "-c",
             "from app import app; "
             "print(app.config['SESSION_COOKIE_SECURE'])"],
            env=env,
            capture_output=True,
            text=True
        )

        label = value if value is not None else "Not specified"

        if expected is None:
            assert result.returncode != 0
            assert "SESSION_COOKIE_SECURE must be true or false" in result.stderr
            print(f"PASS: {label} -> Configuration rejected")
        else:
            assert result.returncode == 0, result.stderr
            assert result.stdout.strip() == str(expected)
            print(f"PASS: {label} -> Secure cookies: {expected}")

print("\nALL 5 COOKIE CONFIGURATION TESTS PASSED")
