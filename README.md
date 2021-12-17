# pyaivchat
AI Voice JP Twitch and YouTube TTS and chatbot. Runs both Twitch and YouTube bots in
parallel but sends the TTS commands sequentially.

Using Python 3.8

Requires installing Assistant Seika and SeikaSay2 for AI Voice JP integration.

Use pipenv to install packages:

```
pipenv install
```

Create a `.env` file with the following:

```
# .env
TOKEN=<twitch_token from twitchio>
BOT_PREFIX=!
CHANNEL=<channel_name>

# YouTube
VID_ID=<stream/vid_id>
```

Log in to Google Cloud Developer console and enable the YouTube API and 
generate a client secret and place it in this directory named `client_secret.json`.

Use pipenv to run this program:

```
pipenv run python pyaivchat.py
```
