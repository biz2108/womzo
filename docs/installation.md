# Installation guide

Womzo is distributed as a ready-built Docker
image through GitHub Container Registry.

You do not need to install Python, Flask, JavaScript
development tools or Git to run the published image.

## Requirements

- A 64-bit Linux Docker host
- Docker Engine and Docker Compose v2
- AMD64 or ARM64 processor architecture
- An available TCP port

Check your Docker installation:

    docker --version
    docker compose version

Check your processor architecture:

    uname -m

Typical supported results are x86_64 and aarch64.

## Create an installation directory

    mkdir worldcams
    cd worldcams

Download compose.yaml and .env.example from the deploy
directory of the corresponding GitHub release.

Save both files in your installation directory using
their original filenames.

## Prepare the configuration

    cp .env.example .env
    chmod 600 .env
    mkdir -m 700 data

Generate two random secrets:

    openssl rand -hex 16
    openssl rand -hex 32

Use the first value as ADMIN_PASSWORD and the second
as SECRET_KEY in your .env file.

Do not retain the example placeholder values.

Determine your Linux user and group IDs:

    id -u
    id -g

Enter the corresponding values for PUID and PGID in .env.

See the [Configuration guide](configuration.md) for
further information.

## Start the application

For initial local HTTP testing, set the following
values in .env:

    BIND_ADDRESS=127.0.0.1
    SESSION_COOKIE_SECURE=false

From your installation directory, run:

    docker compose pull
    docker compose up -d
    docker compose ps

When the container is healthy, open:

http://127.0.0.1:8099

The application starts with an empty webcam collection.

## Access from a headless server

If Docker runs on a different computer, an SSH tunnel
allows you to access the application without exposing
its port to the local network.

From your desktop or laptop, run:

    ssh -N -L 127.0.0.1:8099:127.0.0.1:8099 user@server

Replace user and server with your own SSH username
and server address.

Keep the SSH session open and visit:

http://127.0.0.1:8099

Press Ctrl+C in the SSH terminal to close the tunnel.

## Add your first webcam

1. Select Manage.
2. Sign in using your administrator password.
3. Enter a camera name, location and supported URL.
4. Save the camera.
5. Return to the viewer and select the camera.

Only add sources that you have permission to display.

## Stop or remove the container

To temporarily stop the application:

    docker compose stop

To start it again:

    docker compose start

To remove the container and its Compose network:

    docker compose down

Your data directory and private configuration are
retained on the host.

## Next steps

- Review the [Configuration guide](configuration.md).
- Arrange regular backups of your installation.
- Configure HTTPS before making the application
  accessible over the internet.
