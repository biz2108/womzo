# Third-party software notices

SJB's World Webcams includes third-party open-source
software. Such software retains its respective licences
and copyright notices.

## HLS.js

- Version: 1.7.4
- Licence: Apache License 2.0
- Project: https://github.com/video-dev/hls.js
- Copyright (c) 2017 Dailymotion
- Copyright (c) 2013-2015 Brightcove (derived portions)

The original copyright and licence notice is retained at:

static/vendor/hls.js/LICENSE

The full Apache License 2.0 text is available at:

static/vendor/hls.js/LICENSE-APACHE-2.0.txt

## HLS.js bundled dependencies

The following components were identified through the
HLS.js 1.7.4 source map and dependency lock file.

| Component | Version | Licence |
| --- | --- | --- |
| @babel/helpers | 7.29.7 | MIT |
| eventemitter3 | 5.0.4 | MIT |
| url-toolkit | 2.2.5 | Apache-2.0 |
| @svta/cml-id3 | 1.0.6 | Apache-2.0 |
| @svta/cml-structured-field-values | 1.1.3 | Apache-2.0 |
| @svta/cml-cmcd | 2.4.0 | Apache-2.0 |
| @svta/cml-utils | 1.5.0 | Apache-2.0 |

The CML Utils notice is included as a precaution
because it is a dependency of the SVTA components.

Original licence documents are retained in:

- static/vendor/hls.js/LICENSE-BABEL-MIT.txt
- static/vendor/hls.js/third-party-licenses/

The original copyright notices in the distributed
JavaScript bundle have been preserved.

Package integrity was verified against the HLS.js
v1.7.4 dependency lock file on 19 November 2026.

## Python dependencies

The following Python packages were present in the
reviewed Docker installation on 19 November 2026.

| Package | Version | Licence |
| --- | --- | --- |
| Blinker | 1.9.0 | MIT |
| Click | 8.5.1 | BSD-3-Clause |
| Flask | 3.1.3 | BSD-3-Clause |
| Gunicorn | 27.0.1 | MIT |
| ItsDangerous | 2.2.0 | BSD-3-Clause |
| Jinja2 | 3.1.6 | BSD-3-Clause |
| MarkupSafe | 3.0.4 | BSD-3-Clause |
| pip | 26.3 | MIT |
| Werkzeug | 3.1.9 | BSD-3-Clause |

All retain their original licence and copyright notices
within the reviewed Docker installation.

Direct application dependencies are listed in
requirements.txt. Installed versions may change
when the Docker image is rebuilt.

## Webcam content

Webcam streams, images and other external media remain
the property of their respective rights holders.

The application's software licence does not grant any
rights to third-party media or webcam content.
