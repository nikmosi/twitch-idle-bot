# twitch-idle-bot

A minimal Twitch chat reader. It connects to a Twitch channel and prints the
messages it receives. OAuth tokens are automatically refreshed and stored in
`token.json`.

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency
management and execution. Install uv and fetch the dependencies with:

```bash
pip install uv
uv sync
```

## Usage

Set the required environment variables and run the bot using [`uv`](https://github.com/astral-sh/uv):

```bash
export TWITCH_CLIENT_ID=your_client_id
export TWITCH_CLIENT_SECRET=your_client_secret
export TWITCH_TARGET_CHANNELS=channel_name

uv run main.py
```

### Optional environment variables

The bot also recognizes the following optional variables:

- `TWITCH_FILTERED_NAME` – comma-separated usernames to ignore in chat (default: `gloria_bot,nikmosi`)
- `TWITCH_USER_SCOPE` – comma-separated Twitch scopes (default: `chat:read`)
- `TWITCH_CALLBACK_URL` – OAuth callback URL (default: `http://localhost:8081/login/confirm`)
- `TWITCH_PORT` – port for the authentication server (default: `8000`)
- `TWITCH_STORAGE_PATH` – path to store OAuth tokens (default: `./var/token.json`)

## Tests

Run the test suite with:

```bash
uv run pytest
```
