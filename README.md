# pyaivchat
SeikaSay2 Twitch and YouTube TTS and chatbot. Runs both Twitch and YouTube bots in
parallel but sends the TTS commands sequentially.

# Requirements
Using Python 3.8

Requires installing [AssistantSeika](https://hgotoh.jp/wiki/doku.php/documents/voiceroid/assistantseika/assistantseika-001a)
and using the included SeikaSay2 for AI Voice JP integration.

This was mainly made for the author's purchased [A.I. Voice JP Kotonoha sister's English](https://aivoice.jp/kotonoha/en/)
TTS program, but since AssistantSeika works for VOICEROID(2), CeVIO, AITalk3, etc., this should also work for them
as long as you set up your AssistantSeika properly.

Make sure that wherever you extracted SeikaSay2.exe that you add the folder to your
environment **PATH** variable.

# Installation

Since the above programs are basically Windows only, please install Anaconda. 
After installing Anaconda, create an environment and install pipenv:
```
conda create --name pyaivchat
conda activate pyaivchat
conda install -c conda-forge pipenv
```

Might as well also install specifically Python 3.8 with conda:
```
conda install python=3.8
```

Use pipenv to install packages:

```
pipenv install
```

# Setup

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
generate a client secret, exporting it as a file and place it in this directory named `client_secret.json`.

# Running

Use pipenv to run this program:

```
pipenv run python pyaivchat.py
```

The program will prompt you to generate an OAuth2 token from your bot account on your browser. Do so and YouTube should be integrated as well.
