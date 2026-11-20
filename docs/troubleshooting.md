# Troubleshooting guide

This guide addresses common problems that may arise
when installing or using SJB's World Webcams.

Run Docker commands from your installation directory.

## The application will not start

Check the container status:

    docker compose ps -a

Examine the application logs:

    docker compose logs --tail=100

Validate the Compose configuration:

    docker compose config --quiet

Common causes include:

- Missing .env file
- Invalid or missing configuration values
- Insufficient password or secret key length
- Incorrect data directory permissions
- A host port already in use

Do not publish logs or configuration output without
checking them for private information.

## Permission denied or database errors

Ensure the data directory exists and is writable
by the user configured through PUID and PGID.

Check its ownership:

    ls -ld data
    ls -l data

See the [Configuration guide](configuration.md)
for instructions on correcting ownership.

Do not resolve permission problems by running
the application as root or granting unrestricted
permissions to the data directory.

## Cannot access the application

Check that the container is healthy:

    docker compose ps

For the default localhost configuration, test the
health endpoint directly on the Docker host:

    curl -fsS http://127.0.0.1:8099/healthz

A healthy application returns:

    {"status":"ok"}

Adjust the address and port if you have changed them.

By default, the application is accessible only
from the Docker host under normal conditions.

Use an SSH tunnel or configure network access
as described in the configuration guide.

For reverse proxy installations, also check the
proxy configuration and HTTPS certificate.

## Administrator login does not work

Check that you are using the password configured
in ADMIN_PASSWORD.

If testing over local HTTP, ensure that:

    SESSION_COOKIE_SECURE=false

For HTTPS installations, use:

    SESSION_COOKIE_SECURE=true

After changing the configuration:

    docker compose up -d

Repeated incorrect login attempts can temporarily
trigger the application's rate limiter.

Allow the restriction to expire before trying again.

## No webcams appear after installation

This is expected.

SJB's World Webcams is distributed without a
preconfigured webcam collection.

Select Manage, sign in and add your first camera.

## A webcam does not play

First, use the Original source link to check
whether the original provider is working.

Possible causes include:

- The webcam is temporarily offline.
- The source URL has changed.
- The provider prohibits third-party embedding.
- The provider requires authentication.
- The browser blocks insecure content.
- The video format is unsupported by the browser.
- An HLS provider does not permit cross-origin access.
- A browser extension interferes with playback.
- The provider restricts access by geographic location.

Try another browser or another permitted source
to establish whether the problem affects one camera
or the entire application.

Not every publicly accessible webcam can be embedded.

Do not attempt to bypass a provider's access controls
or embedding restrictions.

## A webcam opens on its original website only

Some sources cannot be displayed directly inside
the application.

For these sources, viewers can follow the
Original source link.

This is intentional behaviour rather than
necessarily an application fault.

## Docker cannot download the image

Check the image name and version in compose.yaml.

The official image repository is:

    ghcr.io/biz2108/sjb-world-webcams

Supported processor architectures are Linux/AMD64
and Linux/ARM64.

The official public release images do not require
a GitHub account for downloading.

Private development images require authentication.

## Changes disappear after recreating a container

Check that the persistent data directory is mounted
correctly and that you are using the original
installation directory.

The application database should be located at:

    data/webcams.sqlite3

Do not delete or replace this directory when
upgrading the application.

Consult the [Maintenance guide](maintenance.md)
for backup and restoration instructions.

## Reporting a problem

If you cannot resolve a problem, visit the project's
GitHub repository:

https://github.com/biz2108/sjb-world-webcams

Useful information for a bug report includes:

- Application version from the About section
- Host operating system
- Processor architecture
- Docker and Docker Compose versions
- Browser and browser version
- Steps required to reproduce the problem
- Relevant, reviewed log messages

Never include passwords, secret keys, access tokens,
private webcam URLs or your complete .env file.

Security vulnerabilities should be reported privately
as described in the contributor guidelines.
