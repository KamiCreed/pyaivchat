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

        if not subcmd:
            sep = ', '
            # List subcommands
            await ctx.send(VOICE_SUB.format(sep.join(list(self.voice_sub.keys()))))
            return

        subcmd = args.pop(0)

        # Invoke subcommand
        await self.voice_sub[subcmd](ctx, args)

    async def _voice_ls(self, ctx: commands.Context, args):
        # List TTS voice keys
        voices = self.seika.get_voices()
        sep = ', '
        await ctx.send(VOICE_LS.format(sep.join(voices))

    async def _voice_change(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_CHANGE_USAGE.format(ctx.prefix))
            #await ctx.send(VOICE_CHANGE_CHECK.format(ctx.prefix))
            return
        
        voice_key = args.pop(0)
        success = self.seika.pick_voice(ctx.author.name, voice_key)
        if success:
            await ctx.send(VOICE_CHANGE_SUCCESS.format(username=ctx.author.name, voice_key=voice_key))
        else:
            await ctx.send(VOICE_CHANGE_FAIL.format(username=ctx.author.name, prefix=ctx.prefix))

        if args:
            await self._voice_speed(ctx, args)
        else:
            self.seika.save()

    async def _voice_speed(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_SPEED_USAGE.format(ctx.prefix))
            return

        try:
            speed = float(args.pop(0))
        except ValueError:
            await ctx.send(VOICE_SPEED_NAN.format(ctx.author.name))

        success = self.seika.pick_speed(speed)
        if success:
            await ctx.send(VOICE_SPEED_SUCCESS.format(ctx.author.name, speed))
        else:
            await ctx.send(VOICE_SPEED_FAIL.format(ctx.author.name))

        if args:
            await self._voice_speed(ctx, args)
        else:
            self.seika.save()

    async def _voice_pitch(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_PITCH_USAGE.format(ctx.prefix))
            return

        try:
            pitch = int(args.pop(0))
        except ValueError:
            await ctx.send(VOICE_PITCH_NAN.format(ctx.author.name))
            return

        success = self.seika.pick_pitch(pitch)
        if success:
            await ctx.send(VOICE_PITCH_SUCCESS.format(ctx.author.name, pitch))
        else:
            await ctx.send(VOICE_PITCH_FAIL.format(ctx.author.name))

        if args:
            await self._voice_inton(ctx, args)
        else:
            self.seika.save()

    async def _voice_inton(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_INTON_USAGE.format(ctx.prefix))
            return

        try:
            inton = int(args.pop(0))
        except ValueError:
            await ctx.send(VOICE_INTON_NAN.format(ctx.author.name))
            return

        success = self.seika.pick_intonation(inton)
        if success:
            self.seika.save()
            await ctx.send(VOICE_INTON_SUCCESS.format(ctx.author.name, inton))
        else:
            await ctx.send(VOICE_INTON_FAIL.format(ctx.author.name))
