# twitch-idle-bot

A minimal Twitch chat reader. It connects to a Twitch channel and prints the
messages it receives. OAuth tokens are automatically refreshed and stored in
`token.json`.

## Usage

Set the required environment variables and run the bot using [`uv`](https://github.com/astral-sh/uv):

```bash
export TWITCH_CLIENT_ID=your_client_id
export TWITCH_CLIENT_SECRET=your_client_secret
export TWITCH_CHANNEL=channel_name
# optional nickname, defaults to an anonymous "justinfan" account
export TWITCH_NICK=your_bot_nickname

uv run main.py
```

## Tests

Run the test suite with:

```bash
uv run pytest
```
