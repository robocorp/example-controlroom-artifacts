# How to access Control Room artifacts

For E2E purposes this repository contains example Robot which take screenshots of web sites.
For E2E purposes this repository contains server implementation which will be accessing webhook events.

## Webhook approach

1. Activate webhook in a Control Room API section. Events to follow would be "Process run" and "Step run".
2. The local server is exposed to the internet using Ngrok. The Ngrok URL needs to be placed into Control Room as a webhook URL.

## Description of the server which is receiving webhook events

Implemented with Python Flask package. The server then reads process details and accesses process artifacts
when event indicating process complete has been received. Server downloads all ".png" named files into
local directory.

Server needs to know Control Room workspace ID and the API key for accessing Process API. In this implementation those are
provided as environment variables `CONTROL_ROOM_WORKSPACE_ID` and `CONTROL_ROOM_WORKSPACE_API_KEY`.

## Description of the example Robot

TBD


## Learning materials

- [Robocorp Developer Training Courses](https://robocorp.com/docs/courses)
- [Documentation links on Robot Framework](https://robocorp.com/docs/languages-and-frameworks/robot-framework)
- [Example bots in Robocorp Portal](https://robocorp.com/portal)
