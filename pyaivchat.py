import os
import argparse
import pytchat
import asyncio

from ytchat import YtChat
from twitchchat import TwitchChat

def start_yt(prefix, vid_id):
    ytchat = YtChat("client_secret.json", vid_id)

    chat = pytchat.create(video_id=vid_id)
    print("Getting chat messages...")
    while chat.is_alive():
        for c in chat.get().sync_items():
            print(f"{c.datetime} [{c.author.name}]- {c.message}")
            if c.message.startswith(prefix):
                cmd = c.message[len(prefix):]
                ytchat.send_message(cmd)

def start_twitch(prefix):
    loop = asyncio.get_event_loop()
    bot = TwitchChat(
        # set up the bot
        token=os.environ['TOKEN'],
        prefix=prefix,
        initial_channels=[os.environ['CHANNEL']]
    )
    bot.run()
    close_task = loop.create_task(bot.close())
    loop.run_until_complete(close_task)
    loop.close()

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
