import os
import pytchat

from ytchat import YtChat
from twitchchat import TwitchChat

def main():
    prefix = os.environ['BOT_PREFIX']
    vid_id = os.environ['VID_ID']

    bot = TwitchChat(
        # set up the bot
        token=os.environ['TOKEN'],
        prefix=prefix,
        initial_channels=[os.environ['CHANNEL']]
    )
    bot.run()
    return

    ytchat = YtChat("client_secret.json", vid_id)

    chat = pytchat.create(video_id=vid_id)
    print("Getting chat messages...")
    while chat.is_alive():
        for c in chat.get().sync_items():
            print(f"{c.datetime} [{c.author.name}]- {c.message}")
            if c.message.startswith(prefix):
                cmd = c.message[len(prefix):]
                ytchat.send_message(cmd)

if __name__ == "__main__":
    main()
