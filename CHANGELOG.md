# Changelog

All notable changes to SJB's World Webcams
will be documented in this file.

## [0.1.1] - Unreleased

### Added

- GNU Affero General Public License v3.0 (AGPL-3.0-only).
- Third-party licensing and copyright documentation.
- Branding and contributor guidelines.
- Webcam permissions and visitor privacy guidance.
- Version-specific GitHub source-code link.
- Improved installation and directory ownership instructions.
- Reusable automated test suite with 19 application and security tests.
- GitHub Actions continuous integration.
- Docker image distribution through GitHub Container Registry.
- Multi-architecture Docker images for AMD64 and ARM64.
- Native runtime testing on both supported architectures.
- Standard OCI Docker image metadata.
- Ready-to-use Docker Compose deployment configuration.
- Dedicated installation, configuration, maintenance and troubleshooting guides.
- Expanded README with quick-start instructions.

### Changed

- Clarified that users create their own webcam collections.
- Recommended installation from ready-built Docker images.
- Restricted the Docker build context to required application files.

### Security

- Strict validation of the secure session cookie setting.

## [0.1.0] - 2026-11-18

Initial internal development baseline.

### Added

- Responsive webcam viewer with search.
- Password-protected administration interface.
- Add, edit, delete and reorder webcams.
- YouTube, IPCamLive, MyEarthCam, HLS and image support.
- Original source links.
- SQLite database storage.
- Docker Compose deployment.
- CSRF protection and login rate limiting.
- Content Security Policy.
- About page, acknowledgements and Ko-fi support.
