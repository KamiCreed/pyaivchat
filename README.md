# pyaivchat
SeikaSay Twitch and YouTube TTS and chatbot. Runs both Twitch and YouTube bots in
parallel but sends the TTS commands sequentially.

Using Python 3.8

Requires installing [AssistantSeika](https://hgotoh.jp/wiki/doku.php/documents/voiceroid/assistantseika/assistantseika-001a)
and [SeikaSay2](https://hgotoh.jp/wiki/lib/exe/fetch.php/documents/voiceroid/assistantseika/seikasay220210807u.zip) for AI Voice JP integration.

This was mainly made for the author's [A.I. Voice JP Kotonoha sister's English](https://aivoice.jp/kotonoha/en/)
TTS program, but since AssistantSeika works for VOICEROID(2), CeVIO, AITalk3, etc., this should also work for them
as long as you set up your AssistantSeika properly.

Since the above programs are basically Windows only, please install Anaconda.

After installing Anaconda, create an environment and install pipenv.
```
conda create --name pyaivchat
conda activate pyaivchat
conda install -c conda-forge pipenv
```

Might as well also install Python 3.8 with conda:
```
conda install python=3.8
```

Use pipenv to install packages:

```
pipenv install
```

Create a new Twitch bot account and get a token from [TwitchIO](https://github.com/TwitchIO/TwitchIO) to integrate Twitch.

Create a new brand YouTube channel and sign into it.

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

The program will prompt you to generate an OAuth2 token from your bot account on your browser. Do so and YouTube should be integrated as well.
