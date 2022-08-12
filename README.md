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

Since the above programs are basically Windows only, please install a python environment such as
[Anaconda](https://www.anaconda.com/download/) or
[Miniconda](https://docs.conda.io/en/latest/miniconda.html). 
After installing `conda`, open up \<Ana/Mini\>conda Prompt, create an environment, and install pipenv:
```
conda create --name pyaivchat python=3.8 pipenv
conda activate pyaivchat
```

For a simple python environment just install `pipenv`:
```
pip install pipenv
```

Navigate to this folder and use pipenv to install packages:

```
pipenv install
```

# Setup

Create a new Twitch bot account and get a token from [TwitchIO](https://github.com/TwitchIO/TwitchIO) to integrate Twitch.

Create a new brand YouTube channel and sign into it.

Create a `.env` file with the following:

```
# .env
# Twitch
TOKEN=<twitch_token from twitchio>
BOT_PREFIX=!
CHANNEL=<channel_name>

# YouTube
CHANNEL_ID=<channel_id>
EVENT_TYPE=<live/upcoming>
```

EVENT\_TYPE can either be `live` or `upcoming` depending on whether you ran this bot while you are
streaming or simply created a YouTube event in anticipation. `upcoming` only looks for the most recent
_publicly_ published livestream event.

Log in to Google Cloud Developer console and enable the YouTube API and [generate a client
secret](https://developers.google.com/youtube/registering_an_application), exporting it as a file and place it
in this directory named `client_secret.json`.

# Running

Open up A.I. Voice editor (Or a supported TTS progam) and setup AssistantSeika (They must both be running for
this bot to work).

Use pipenv to run this program:

```
pipenv run python pyaivchat.py
```

The program will prompt you to generate an OAuth2 token from your bot account on your browser. Do so and
YouTube should be properly integrated.

The chat commands are as follows:
```
<prefix>voice
```

# Troubleshooting

This is not for this program persay but if you also bought the A.I. VOICE Kotonoha English voices, you
may have to install a trial version of one of the other voices [on their site](https://aivoice.jp/member/downloads/trial) in order for
AssistantSeika to recognize them. This may be due to missing JP packages that the English
install doesn't include, which the AssistantSeika developer may not have accounted for. Installing one or the other first
shouldn't really matter, but I did install the JP trial after I installed the English version.
