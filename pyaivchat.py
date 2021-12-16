import os
import argparse

from ytchat import YtChat
from twitchchat import TwitchChat

def start_yt(prefix, vid_id):
    ytchat = YtChat(secret_file="client_secret.json", vid_id=vid_id, prefix=prefix)
    ytchat.run()

def start_twitch(prefix):
    bot = TwitchChat(
        # set up the bot
        token=os.environ['TOKEN'],
        prefix=prefix,
        initial_channels=[os.environ['CHANNEL']]
    )
    bot.run()

def main():
    prefix = os.environ['BOT_PREFIX']
    vid_id = os.environ['VID_ID']

    parser = argparse.ArgumentParser(description='Twitch or YouTube chatbot and SeikaSay TTS')
    parser.add_argument('--yt', action='store_true', help='Run YouTube chatbot instead of Twitch')
    args = parser.parse_args()

    if args.yt:
        start_yt(prefix, vid_id)
    else:
        start_twitch(prefix)

    print("End.")


if __name__ == "__main__":
    main()
