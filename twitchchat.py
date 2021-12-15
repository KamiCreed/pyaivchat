from twitchio.ext import commands
import subprocess
from seikapick import SeikaPick

from consts import *

class TwitchChat(commands.Bot):

    def __init__(self, token, prefix, initial_channels):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix=prefix, initial_channels=initial_channels)

        self.prefix = prefix
        self.seika = SeikaPick()

        self.voice_sub = {
                'ls': self._voice_ls,
                'change': self._voice_change,
                'pitch': self._voice_pitch,
                'speed': self._voice_speed,
                'inton': self._voice_inton,
                }

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.author.name, message.content)

        if not message.content.startswith(self.prefix) and not message.content.startswith('!'):
            self.seika.say_for_user(message.author.name, message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def voice(self, ctx: commands.Context):
        cmd = f"{ctx.prefix}voice"

        args = ctx.message.content.split()
        # Remove command
        args.pop(0)

        subcmd = args.pop(0)

        # Invoke subcommand
        await self.voice_sub[subcmd](ctx, args)

    async def _voice_ls(self, ctx: commands.Context, args):
        # List TTS voice keys
        voices = self.seika.get_voices()
        sep = ', '
        await ctx.send(f'Avail voices: {sep.join(voices)}')

    async def _voice_change(self, ctx: commands.Context, args):
        await ctx.send(f'Hello {ctx.author.name}!')

    async def _voice_speed(self, ctx: commands.Context, args):
        await ctx.send(f'Hello {ctx.author.name}!')

    async def _voice_pitch(self, ctx: commands.Context, args):
        await ctx.send(f'Hello {ctx.author.name}!')

    async def _voice_inton(self, ctx: commands.Context, args):
        await ctx.send(f'Hello {ctx.author.name}!')
