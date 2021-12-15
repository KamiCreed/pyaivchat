import os
import pytchat
import configparser
from ytchat import YtChat
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self, token, prefix, initial_channels):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix=prefix, initial_channels=initial_channels)

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

def main():
    prefix = os.environ['BOT_PREFIX']
    vid_id = os.environ['VID_ID']

    bot = Bot(
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
