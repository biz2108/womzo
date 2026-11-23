# Maintenance guide

Womzo is designed to require very little
routine maintenance.

All commands in this guide should be run from your
application installation directory unless otherwise stated.

## Checking application status

    docker compose ps

The container should normally report a healthy status.

To examine recent application logs:

    docker compose logs --tail=100

To follow logs in real time:

    docker compose logs -f

Press Ctrl+C to stop following the logs.

## What to back up

Your installation contains three important components:

| File or directory | Contents |
| --- | --- |
| data/ | Webcam database and associated SQLite files |
| .env | Private application configuration |
| compose.yaml | Docker deployment configuration |

The Docker image itself can normally be downloaded
again from GitHub Container Registry.

## Creating a backup

Stop the application before copying its database
to ensure a consistent file-based backup.

From your installation directory:

    docker compose stop

Create a private backup directory outside the
application installation:

    BACKUP_DIR="$(mktemp -d "$HOME/worldcams-backup.XXXXXXXX")"

Create the backup archive:

    (umask 077; tar -czf "$BACKUP_DIR/worldcams.tar.gz" data .env compose.yaml)

Check that the archive was created successfully:

    tar -tzf "$BACKUP_DIR/worldcams.tar.gz"

Restart the application:

    docker compose start
    docker compose ps

Make sure the application has restarted, even if
the backup procedure encountered an error.

Store a copy of the backup on another disk, NAS
or suitable backup service.

Backups contain private configuration and must
be protected against unauthorised access.

## Restoring a backup

Stop the existing installation before attempting
a restoration.

Keep a separate copy of the current installation
in case the restoration needs to be reversed.

The safest approach is to extract the backup into
a new, empty installation directory.

For example:

    mkdir -m 700 worldcams-restored
    cd worldcams-restored
    tar -xzf /path/to/worldcams.tar.gz

Replace the example archive path with the actual
location of your backup.

Check that the data directory, .env and compose.yaml
have been restored.

Ensure the configured container user can write
to the data directory.

Do not start the restored installation while another
installation is using the same host port.

Start the restored application:

    docker compose up -d
    docker compose ps

Confirm that your webcam collection and administrator
access have been restored successfully.

## Upgrading the application

The supplied Compose file uses a numbered image
version to avoid unexpected upgrades.

Before upgrading:

1. Read the release notes.
2. Create a complete backup.
3. Edit compose.yaml.
4. Replace the existing image tag with the new release.

Download the new image:

    docker compose pull

If the download succeeds, recreate the container:

    docker compose up -d
    docker compose ps

Check the viewer, administrator interface and saved
webcam collection.

The About section displays the application version.

## Rolling back an upgrade

If an upgrade causes problems, consult the release
notes before returning to an earlier version.

Some future releases may introduce database changes
that are incompatible with earlier versions.

If necessary, restore the complete pre-upgrade backup,
including its original Compose file and database.

## Changing the administrator password

Generate a new random password:

    openssl rand -hex 16

Update ADMIN_PASSWORD in .env.

To invalidate existing authenticated sessions, also
generate a new SECRET_KEY:

    openssl rand -hex 32

Apply the new configuration:

    docker compose up -d

Store the new credentials securely.

## Routine maintenance

- Check for new application releases periodically.
- Maintain regular backups.
- Occasionally test your restoration procedure.
- Remove webcam entries that no longer work.
- Keep Docker and the host operating system updated.
- Review your reverse proxy and firewall configuration.

Automatic application upgrades are optional and
should not replace a reliable backup procedure.
