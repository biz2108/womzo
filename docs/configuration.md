# Configuration guide

Application settings are stored in the private .env
file in your installation directory.

Never publish or share this file.

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| ADMIN_PASSWORD | Required | Administrator password |
| SECRET_KEY | Required | Session signing key |
| PUID | 1000 | Container user ID |
| PGID | 1000 | Container group ID |
| SESSION_COOKIE_SECURE | true | Require HTTPS for session cookies |
| BIND_ADDRESS | 127.0.0.1 | Host network binding |

## Administrator password

Use a randomly generated password containing at least
16 characters.

A suitable password can be generated with:

    openssl rand -hex 16

Store the password securely in a password manager.

## Secret key

The secret key protects the integrity of application
session cookies.

Use a randomly generated value containing at least
32 characters.

    openssl rand -hex 32

Changing the secret key invalidates existing sessions.

Do not reuse your administrator password as the
secret key.

## User and group IDs

The application is designed to run as a non-root user.

PUID and PGID determine the identity under which the
container operates.

The configured user must be able to write to the
persistent data directory.

To determine your current user and group IDs:

    id -u
    id -g

If you deliberately use your own Linux user's IDs,
the following commands can correct the ownership
of the installation's data directory:

    sudo chown -R "$(id -u):$(id -g)" data
    chmod 700 data

Run these commands from the installation directory.

## Network binding

### Localhost

    BIND_ADDRESS=127.0.0.1

This is the recommended default. It restricts normal
access to the Docker host itself.

Use an SSH tunnel for convenient remote access.

### Local network

To allow access from other devices, configure
BIND_ADDRESS with the Docker host's LAN IP address.

Apply appropriate firewall restrictions.

Anyone who can access the viewer can see the saved
camera URLs.

HTTPS is recommended for administration, even on
local networks.

### Reverse proxy

For an internet-facing installation, use a reverse
proxy with a valid HTTPS certificate.

If the proxy runs directly on the Docker host,
localhost binding may be suitable.

If the proxy runs on another machine, bind to the
appropriate LAN address and restrict direct access
to the reverse proxy.

Do not forward the application's Docker port directly
to the internet.

An additional authentication layer protecting
administration is recommended.

## Secure session cookies

For HTTPS installations:

    SESSION_COOKIE_SECURE=true

For trusted local-only HTTP testing or SSH tunnels:

    SESSION_COOKIE_SECURE=false

Never expose HTTP-only administration directly
to the internet.

Only true and false are accepted as values.

## Changing the published port

The supplied Compose file uses host port 8099.

If this port is already in use, change the host-side
port number in the ports section of compose.yaml.

Leave the internal container port at 8000.

For example, to use host port 8100:

    ports:
      - "${BIND_ADDRESS:-127.0.0.1}:8100:8000"

Adjust your browser address, SSH tunnel or reverse
proxy configuration accordingly.

## Applying configuration changes

After editing .env or compose.yaml, run:

    docker compose config --quiet
    docker compose up -d
    docker compose ps

Do not share the output of docker compose config
without reviewing it, as it may contain private
environment values.

## Persistent storage

The application database is stored in:

    data/webcams.sqlite3

The supplied Compose configuration mounts the data
directory into the container at /data.

Retain this directory when replacing or upgrading
the container.
