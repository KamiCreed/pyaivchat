from twitchio.ext import commands
import subprocess
import re
import traceback

from seikapick import SeikaPick

from consts import *

class TwitchChat(commands.Bot):
    invalid_unicode_re = re.compile(u'[\U000e0000\U000e0002-\U000e001f]', re.UNICODE)
    spam_filter_re = re.compile(SPAM_FILTER_RE, flags=re.I)

    def __init__(self, token, prefix, initial_channels, tts_queue):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix=prefix, initial_channels=initial_channels)

        self.prefix = prefix
        self.seika = SeikaPick(tts_queue)

        self.voice_sub = {
                'ls': self._voice_ls,
                'change': self._voice_change,
                'pitch': self._voice_pitch,
                'speed': self._voice_speed,
                'inton': self._voice_inton,
                'show': self._voice_show,
                }

    def replace_invalid_unicode(self, text, replacement_char=u'\uFFFD'):
        return self.invalid_unicode_re.sub(replacement_char, text)

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        filtered_content = self.spam_filter_re.sub(r'\2\6', message.content)

        # Print the contents of our message to console...
        print(message.author.name, message.content)
        print(message.author.name, filtered_content)

        if not message.content.startswith(self.prefix) and not message.content.startswith('!'):
            self.seika.say_for_user(message.author.name, filtered_content)

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

        content = self.replace_invalid_unicode(ctx.message.content, '')
        args = content.split()
        # Remove command
        args.pop(0)

        if not args:
            sep = ', '
            print("Listing subcommands...")
            # List subcommands
            await ctx.send(VOICE_SUB.format(prefix=ctx.prefix, keys=sep.join(list(self.voice_sub.keys()))))
            return

        subcmd = args.pop(0)

        # Invoke subcommand
        await self.voice_sub[subcmd](ctx, args)

    async def _voice_ls(self, ctx: commands.Context, args):
        # List TTS voice keys
        voices = self.seika.get_voices()
        sep = ', '
        await ctx.send(VOICE_LS.format(username=ctx.author.name, voices=sep.join(voices)))

    async def _voice_change(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_CHANGE_USAGE.format(prefix=ctx.prefix))
            #await ctx.send(VOICE_CHANGE_CHECK.format(prefix=ctx.prefix))
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
            await ctx.send(VOICE_SPEED_USAGE.format(prefix=ctx.prefix))
            return

        try:
            speed = float(args.pop(0))
        except ValueError:
            traceback.print_exc()
            await ctx.send(VOICE_SPEED_NAN.format(username=ctx.author.name))

        success = self.seika.pick_speed(ctx.author.name, speed)
        if success:
            await ctx.send(VOICE_SPEED_SUCCESS.format(username=ctx.author.name, speed=speed))
        else:
            await ctx.send(VOICE_SPEED_FAIL.format(username=ctx.author.name))

        if args:
            await self._voice_speed(ctx, args)
        else:
            self.seika.save()

    async def _voice_pitch(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_PITCH_USAGE.format(prefix=ctx.prefix))
            return

        try:
            pitch = float(args.pop(0))
        except ValueError:
            traceback.print_exc()
            await ctx.send(VOICE_PITCH_NAN.format(username=ctx.author.name))
            return

        success = self.seika.pick_pitch(ctx.author.name, pitch)
        if success:
            await ctx.send(VOICE_PITCH_SUCCESS.format(username=ctx.author.name, pitch=pitch))
        else:
            await ctx.send(VOICE_PITCH_FAIL.format(username=ctx.author.name))

        if args:
            await self._voice_inton(ctx, args)
        else:
            self.seika.save()

    async def _voice_inton(self, ctx: commands.Context, args):
        if not args:
            await ctx.send(VOICE_INTON_USAGE.format(prefix=ctx.prefix))
            return

        try:
            inton = float(args.pop(0))
        except ValueError:
            traceback.print_exc()
            await ctx.send(VOICE_INTON_NAN.format(username=ctx.author.name))
            return

        success = self.seika.pick_intonation(ctx.author.name, inton)
        if success:
            self.seika.save()
            await ctx.send(VOICE_INTON_SUCCESS.format(username=ctx.author.name, inton=inton))
        else:
            await ctx.send(VOICE_INTON_FAIL.format(username=ctx.author.name))

    async def _voice_show(self, ctx: commands.Context, args):
        try:
            voice_key, speed, pitch, inton = self.seika.get_params(ctx.author.name)
            await ctx.send(VOICE_SHOW.format(username=ctx.author.name, voice_key=voice_key, 
                speed=speed, pitch=pitch, inton=inton))
        except KeyError:
            traceback.print_exc()
            await ctx.send(VOICE_SHOW_FAIL.format(username=ctx.author.name))
