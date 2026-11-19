
# SJB's World Webcams

A free, lightweight, self-hosted webcam viewer built with Flask, JavaScript and Docker.

SJB's World Webcams brings together interesting webcams from around the world in one convenient interface.

Browse locations, select a camera and watch without having to visit numerous different websites.

## Features

- Simple, responsive dark-themed interface
- Search cameras by name or location
- Select a webcam to start playback
- Rearrange cameras into your preferred order
- Password-protected administration
- Add, edit and remove cameras
- Persistent SQLite database
- Docker Compose deployment
- Health checks and non-root execution
- Locally hosted HLS.js library
- No account required for viewers

## Supported sources

The application currently supports:

- YouTube videos and live streams
- Direct HLS streams (.m3u8)
- Direct camera images
- IPCamLive embedded players
- MyEarthCam embedded players
- Links to external webcam websites

Not every webcam can be embedded. Some providers restrict playback, require authentication or prohibit third-party embedding.

When a source cannot be embedded, viewers can use the Original source link.

## How it works

The application stores webcam details in a local SQLite database.

Video streams are fetched directly by the visitor's browser from the original provider. The application does not proxy, download or redistribute video streams.

Only the selected camera is loaded.

## Webcam permissions and privacy

This application is distributed without a preconfigured
webcam collection.

Administrators are responsible for ensuring that they
have permission to display the cameras they add.

Respect the original providers' terms of use, copyright
and embedding restrictions. Public availability does not
necessarily imply permission to embed a stream.

Do not attempt to circumvent access or embedding restrictions.

All saved camera URLs are visible to visitors.
Never add confidential URLs, access tokens, credentials
or private security cameras to a public installation.

Visitors connect directly to third-party providers,
whose respective privacy policies may apply.

## Installation

Docker Engine and Docker Compose are required.

After obtaining the source code, open the project directory.

Create your private environment file and data directory:

```bash
cp .env.example .env
chmod 600 .env
mkdir -p data
```

Edit `.env` and replace the placeholder administrator
password and secret key with strong, randomly generated
values.

Never publish or share your `.env` file.

Determine your Linux user and group IDs:

    id -u
    id -g

Set PUID and PGID in .env to the respective values
returned by these commands.

The data directory must be writable by that user.
For a new installation, creating the directory as
your normal Linux user should be sufficient.

If its ownership needs correcting, run the following
as the user whose IDs you configured:

    sudo chown -R "$(id -u):$(id -g)" data
    chmod 700 data

Use a non-root user for the container.

### Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| ADMIN_PASSWORD | Required | Administrator password |
| SECRET_KEY | Required | Flask session signing key |
| PUID | 1000 | Container user ID |
| PGID | 1000 | Container group ID |
| SESSION_COOKIE_SECURE | true | Require HTTPS for session cookies |
| BIND_ADDRESS | 127.0.0.1 | Host IP address for the published port |

### Network access

By default, the application is accessible on the
Docker host at http://127.0.0.1:8099.

For access from other devices, configure BIND_ADDRESS
with your server's LAN IP address.

For internet-facing installations, use HTTPS through
a reverse proxy and restrict direct access to port 8099.

If your reverse proxy runs on another machine,
configure BIND_ADDRESS with an appropriate LAN address.

For a trusted, local-only HTTP installation, set
SESSION_COOKIE_SECURE=false in .env.

Never expose an HTTP-only administration interface
directly to the internet.

### Start the application

```bash
docker compose up -d --build
docker compose ps
```

Once the container is healthy, open the application
using your configured address.

## Administration

Select **Manage** to sign in.

The administrator can:

- Add webcams
- Edit camera details
- Delete cameras
- Change their display order

Visitors can watch webcams without signing in.

## Data and backups

Camera information is stored in:

`data/webcams.sqlite3`

The database is preserved across Docker container rebuilds through a persistent volume.

Back up the `data` directory and your private configuration separately.

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

For internet-facing deployments, HTTPS and an additional authentication layer for administration are recommended.

## Acknowledgements

All webcam streams remain the property of their respective owners and providers.

We appreciate the individuals and organisations that make these views publicly available.

This project uses HLS.js, distributed under the Apache License 2.0 licence. Its licence is included with the distributed library.

Created by SJB with development assistance from ChatGPT.

## Support

SJB's World Webcams is free to use.

If you enjoy the project and would like to support its continued development, you can buy me a coffee:

https://ko-fi.com/sjbprojects

## Development

SJB's World Webcams is an SJB Projects application.

Additional platform support, documentation and distribution options are planned.

## Licence

Copyright (C) 2026 SJB.

SJB's World Webcams is licensed under the GNU Affero
General Public License version 3.0 (AGPL-3.0-only).

See [LICENSE](LICENSE) for the full licence terms.

Third-party components retain their respective licences.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
for further information.

## Branding

SJB's World Webcams is published under the SJB Projects
identity.

See our [Branding Policy](BRANDING.md) for guidance on
the use of project names, logos and branding.

## Contributing

Community contributions, bug reports and suggestions
are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance
on contributing to the project.
