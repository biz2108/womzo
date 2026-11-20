#!/usr/bin/env bash

# Copyright (C) 2026 SJB
# SPDX-License-Identifier: AGPL-3.0-only

set -Eeuo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$(mktemp -d /tmp/worldcams-test.XXXXXXXX)"
PROJECT="worldcams-test-$(basename "$TEST_DIR" | tr '[:upper:]' '[:lower:]' | cut -d. -f2)"

compose() {
    docker compose \
        --project-name "$PROJECT" \
        --project-directory "$TEST_DIR" \
        --env-file "$TEST_DIR/.env" \
        -f "$TEST_DIR/docker-compose.yml" "$@"
}

cleanup() {
    local result=$?
    trap - EXIT

    echo
    echo "Cleaning up isolated test environment..."

    if [[ -f "$TEST_DIR/docker-compose.yml" && -f "$TEST_DIR/.env" ]]; then
        if ! compose down --rmi local --remove-orphans; then
            echo "Cleanup failed. Retained directory: $TEST_DIR"
            exit 1
        fi
    fi

    rm -rf -- "$TEST_DIR"

    if [[ "$result" -eq 0 ]]; then
        echo "SUCCESS: All tests passed and cleanup completed."
    else
        echo "FAILURE: Tests did not complete successfully."
    fi

    exit "$result"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "Preparing isolated test environment: $PROJECT"

cd "$SOURCE_DIR"

cp -a \
    app.py VERSION LICENSE THIRD_PARTY_NOTICES.md \
    requirements.txt Dockerfile docker-compose.yml \
    .dockerignore templates static tests \
    "$TEST_DIR/"

cd "$TEST_DIR"

mkdir data
chmod 700 data

export BIND_ADDRESS=127.0.0.1
export PUID="$(id -u)"
export PGID="$(id -g)"

python3 - <<'PY'
import os
import secrets
from pathlib import Path

Path(".env").write_text(
    f"ADMIN_PASSWORD={secrets.token_hex(16)}\n"
    f"SECRET_KEY={secrets.token_hex(32)}\n"
    f"PUID={os.getuid()}\n"
    f"PGID={os.getgid()}\n"
    "SESSION_COOKIE_SECURE=false\n"
    "BIND_ADDRESS=127.0.0.1\n"
)

Path(".env").chmod(0o600)

path = Path("docker-compose.yml")
content = path.read_text()

assert "    container_name: webcam-directory\n" in content
assert ":8099:8000" in content

content = content.replace(
    "    container_name: webcam-directory\n", ""
)

content = content.replace(":8099:8000", ":18099:8000")
content = content.replace("restart: unless-stopped", 'restart: "no"')

image = os.environ.get("WORLDCAMS_TEST_IMAGE", "")
if image:
    import json
    assert "    build: .\n" in content
    content = content.replace(
        "    build: .\n",
        "    image: " + json.dumps(image) + "\n"
        "    pull_policy: never\n"
    )
path.write_text(content)
PY

echo
echo "Building and starting test container..."

if [[ -n "${WORLDCAMS_TEST_IMAGE:-}" ]]; then
    echo "Testing existing image: $WORLDCAMS_TEST_IMAGE"
    docker image inspect "$WORLDCAMS_TEST_IMAGE" >/dev/null
    compose up -d --wait --wait-timeout 120
else
    compose up -d --build --wait --wait-timeout 120
fi

echo
echo "Running functional tests..."

python3 tests/test_http.py .env

echo
echo "Running security configuration tests..."

compose exec -T webcam-directory python - < tests/test_config.py

echo
echo "ALL 19 AUTOMATED TESTS PASSED"
