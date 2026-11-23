# Womzo

A free, lightweight, self-hosted webcam viewer built with
Flask, JavaScript and Docker.

Womzo allows you to create and manage your own
personal collection of webcams from around the world in one
convenient interface.

Explore distant places, revisit familiar locations, watch
harbours, city skylines, wildlife and more — all without
having to visit numerous different websites.

**Your collection, your choice.**

The application starts with an empty webcam collection.
No webcam links are preinstalled, allowing you to choose
which cameras and supported video sources you wish to add
through the built-in administration interface.

Once configured, visitors can browse locations, search for
cameras and watch their favourites without needing an account.

## Features

- Free and open-source software
- Simple, responsive dark-themed interface
- Desktop and mobile browser support
- Search cameras by name or location
- Select a webcam to start playback
- Rearrange cameras into your preferred order
- Password-protected administration
- Add, edit and remove cameras
- Persistent SQLite database
- Ready-built Docker images
- AMD64 and ARM64 support
- Health checks and non-root execution
- Locally hosted HLS.js library
- No account required for viewers
- No subscription required

## Supported sources

The application currently supports:

- YouTube videos and live streams
- Direct HLS streams (.m3u8)
- Direct camera images
- IPCamLive embedded players
- MyEarthCam embedded players
- Links to external webcam websites

Although designed primarily for webcams, the application
can also be used to organise supported live news streams,
wildlife cameras and other video sources.

Not every webcam can be embedded. Some providers restrict
playback, require authentication or prohibit third-party
embedding.

When a source cannot be embedded, viewers can use the
Original source link.

## Documentation

| Guide | Description |
| --- | --- |
| [Installation](docs/installation.md) | Install and start the application |
| [Configuration](docs/configuration.md) | Application settings, networking and security |
| [Maintenance](docs/maintenance.md) | Backups, restoration and upgrades |
| [Troubleshooting](docs/troubleshooting.md) | Common problems and solutions |

## Installation

### Requirements

- Docker Engine
- Docker Compose v2
- A 64-bit Linux Docker host
- An available TCP port (8099 by default)

Published images support:

| Architecture | Typical hardware |
| --- | --- |
| AMD64 | Intel and AMD PCs, mini PCs and servers |
| ARM64 | Raspberry Pi 4/5 with a 64-bit OS and other ARM64 servers |

Both architectures have undergone automated runtime testing
on native hardware.

### Quick start

Installing the ready-built Docker image from GitHub
Container Registry is the recommended method.

Create a dedicated installation directory:

    mkdir worldcams
    cd worldcams

Download these two files into that directory:

- [compose.yaml](deploy/compose.yaml)
- [.env.example](deploy/.env.example)

Save them using their original filenames.

Create your private configuration and data directory:

    cp .env.example .env
    chmod 600 .env
    mkdir -m 700 data

Generate a random administrator password and session key:

    openssl rand -hex 16
    openssl rand -hex 32

If OpenSSL is unavailable, use a trusted password generator
to create suitably strong random values.

Edit .env using your preferred text editor.

Replace ADMIN_PASSWORD with the first generated value and
SECRET_KEY with the second generated value.

Determine your Linux user and group IDs:

    id -u
    id -g

Set PUID and PGID in .env to the respective values returned
by these commands. Use a non-root user.

Never publish or share your .env file.

For initial testing over local HTTP, set:

    SESSION_COOKIE_SECURE=false
    BIND_ADDRESS=127.0.0.1

This configuration is intended for local testing only.

Start the application:

    docker compose up -d
    docker compose ps

Once the container is healthy, open:

http://127.0.0.1:8099

This address is accessible from the Docker host itself.
For a headless server, use an SSH tunnel or configure
network access as described below.

### Your first webcam

1. Open the application in your browser.
2. Select Manage.
3. Sign in using your administrator password.
4. Enter a camera name, location and supported source URL.
5. Save the camera.
6. Return to the viewer and select your new camera.

Only add sources that you have permission to display.

Visitors can watch the configured webcams without signing in.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| ADMIN_PASSWORD | Required | Administrator password, minimum 16 characters |
| SECRET_KEY | Required | Session signing key, minimum 32 characters |
| PUID | 1000 | Container user ID |
| PGID | 1000 | Container group ID |
| SESSION_COOKIE_SECURE | true | Require HTTPS for session cookies |
| BIND_ADDRESS | 127.0.0.1 | Host IP address for the published port |

The data directory must be writable by the configured user
and group.

If ownership needs correcting, assign the directory to the
Linux user whose IDs you configured.

## Network access

The default binding of 127.0.0.1 prevents direct access
from other devices on the network under normal conditions.

For access from another computer, an SSH tunnel can be used
without changing the application's network binding.

For trusted local network access, configure BIND_ADDRESS
with your Docker host's LAN IP address.

HTTPS is recommended for administration, including on
local networks.

For internet-facing installations:

- Use HTTPS through a reverse proxy.
- Set SESSION_COOKIE_SECURE=true.
- Restrict direct access to the published Docker port.
- Consider an additional authentication layer for administration.

If your reverse proxy runs on another machine, configure
BIND_ADDRESS with an appropriate LAN address and restrict
access to the reverse proxy.

Never expose an HTTP-only administration interface directly
to the internet.

## How it works

The application stores webcam details in a local SQLite
database.

Video streams are fetched directly by the visitor's browser
from the original provider. The application does not proxy,
download or redistribute video streams.

Only the selected camera is loaded.

The application itself does not require an external account
or centralised service.

## Webcam permissions and privacy

This application is distributed without a preconfigured
webcam collection.

Administrators are responsible for ensuring that they have
permission to display the cameras they add.

Respect the original providers' terms of use, copyright
and embedding restrictions. Public availability does not
necessarily imply permission to embed a stream.

Do not attempt to circumvent access or embedding restrictions.

All saved camera URLs are visible to visitors.

Never add confidential URLs, access tokens, credentials or
private security cameras to a public installation.

Visitors connect directly to third-party providers, whose
respective privacy policies may apply.

## Data and backups

Camera information is stored in:

    data/webcams.sqlite3

The database is preserved when containers are removed,
recreated or upgraded because the data directory is stored
outside the container.

Back up the data directory, Compose file and private
environment configuration.

For a consistent file-based database backup, stop the
application before copying its data directory.

Protect backups containing passwords and session keys.

## Updates

The supplied deployment Compose file uses an explicit
application version rather than a moving latest tag.

Before upgrading:

1. Read the release notes.
2. Back up your data and configuration.
3. Change the image version in compose.yaml.
4. Download and start the new image.

    docker compose pull
    docker compose up -d
    docker compose ps

Your existing data directory and private configuration
should be retained.

## Security

The application includes:

- Password-protected administration
- CSRF protection
- Login attempt rate limiting
- Secure session cookie configuration
- Content Security Policy
- Input and URL validation
- Non-root Docker execution
- Restricted container privileges
- Read-only container filesystem

These measures complement, rather than replace, appropriate
network security, HTTPS and responsible server administration.

## Building from source

Building from source is available for developers and users
who prefer to build their own Docker images.

Clone the repository:

    git clone https://github.com/biz2108/sjb-world-webcams.git
    cd sjb-world-webcams

For a particular release, check out its corresponding Git tag.

Prepare .env and the data directory using the configuration
instructions above.

The root docker-compose.yml builds the application locally.
The Compose file in deploy/ instead uses a published image.

To build and start from source, run from the repository root:

    docker compose up -d --build
    docker compose ps

## Automated testing

The project includes a reusable automated test suite covering
application functionality, authentication, CSRF protection
and security configuration.

Requirements:

- Linux with Bash and Python 3
- Docker with a recent Docker Compose v2 plugin
- Permission to run Docker commands
- Local TCP port 18099 available

From the repository directory, run:

    bash tests/run_tests.sh

The test runner creates an isolated Docker installation
with randomly generated credentials and an empty database.

It does not require access to an existing installation
or its credentials.

The temporary test environment is automatically removed
when testing finishes successfully. Docker's reusable build
cache is retained.

The current suite contains:

- 14 functional tests
- 5 secure-cookie configuration tests

GitHub Actions provides three workflows:

| Workflow | Purpose |
| --- | --- |
| Continuous Integration | Automatically test source code changes |
| Publish Development Image | Manually build and publish multi-architecture development images |
| Test Published Docker Image | Test a published image on native AMD64 and ARM64 runners |

Browser-based video playback and production HTTPS behaviour
require separate testing.

## Acknowledgements

All webcam streams remain the property of their respective
owners and providers.

We appreciate the individuals and organisations that make
these views publicly available.

This project uses HLS.js, distributed under the Apache
License 2.0. Its licence is included with the distributed library.

Created by SJB with development assistance from ChatGPT.

## Support

Womzo is free to use.

If you enjoy the project and would like to support its
continued development, you can buy me a coffee:

https://ko-fi.com/sjbprojects

## Development

Womzo is an SJB Projects application.

Additional platform support and improvements are planned.

See the [Changelog](CHANGELOG.md) for version history.

## Licence

Copyright (C) 2026 SJB.

Womzo is licensed under the GNU Affero General
Public License version 3.0 (AGPL-3.0-only).

See [LICENSE](LICENSE) for the full licence terms.

Third-party components retain their respective licences.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
for further information.

## Source-code availability

The About section links to the corresponding tagged release
of the original application on GitHub.

Operators of modified versions must update this link to
provide the corresponding source code of their modified
application in accordance with the AGPL.

## Branding

Womzo is published under the SJB Projects identity.

See our [Branding Policy](BRANDING.md) for guidance on the
use of project names, logos and branding.

## Contributing

Community contributions, bug reports and suggestions
are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance
on contributing to the project.
