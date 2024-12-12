import asyncio
import pytchat
import logging
import traceback
import re

from seikapick import SeikaPick
from consts import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

# TODO: Refactor with a super class
class YtChat:
    spam_filter_re = re.compile(SPAM_FILTER_RE, flags=re.I)

    def __init__(self, 
            secret_file,
            vid_id,
            prefix,
            tts_queue,
            ytauth,
            loop: asyncio.AbstractEventLoop = None,
            ):
        self._ytauth = ytauth
        self._vid_id = vid_id

        self.prefix = prefix
        self.seika = SeikaPick(tts_queue, key=KEY_YOUTUBE)

        self._cmds = {
                'voice': self.voice
                }

        self.voice_sub = {
                'ls': self._voice_ls,
                'change': self._voice_change,
                'pitch': self._voice_pitch,
                'speed': self._voice_speed,
                'inton': self._voice_inton,
                'show': self._voice_show,
                }

        # Hardcode bot names
        self.bot_names = ['Shiori Bot']

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        print("Getting chat messages...")
        chat = pytchat.create(video_id=self._vid_id)
        while chat.is_alive():
            for ctx in chat.get().sync_items():
                print(f"{ctx.datetime} [{ctx.author.name}]- {ctx.message}")
                try:
                    await self._parse(ctx)
                except Exception:
                    traceback.print_exc()
                    logging.info("Ignoring exception...")

    async def _parse(self, ctx):
        if ctx.author.name in self.bot_names:
            return

        filtered_content = self.spam_filter_re.sub(r'\2\6', ctx.message)
        logging.info(filtered_content)

        if not ctx.message.startswith(self.prefix) and not ctx.message.startswith('!'):
            self.seika.say_for_user(ctx.author.name, filtered_content)
            return

        if ctx.message.startswith(self.prefix):
            msg_str = ctx.message[len(self.prefix):]
            args = msg_str.split()
            cmd = args.pop(0)
            try:
                await self._cmds[cmd](ctx)
            except Exception:
                traceback.print_exc()
                print("Ignoring and continuing...")

    async def send(self, msg):
        await self._ytauth.send(msg, self._vid_id)

    async def voice(self, ctx):
        cmd = f"{self.prefix}voice"

        args = ctx.message.split()
        # Remove command
        args.pop(0)

        if not args:
            sep = ', '
            # List subcommands
            await self.send(VOICE_SUB.format(prefix=self.prefix, keys=sep.join(list(self.voice_sub.keys()))))
            return

        subcmd = args.pop(0)

        # Invoke subcommand
        await self.voice_sub[subcmd](ctx, args)

    async def _voice_ls(self, ctx, args):
        # List TTS voice keys
        voices = self.seika.get_voices()
        sep = ', '
        await self.send(VOICE_LS.format(username=ctx.author.name, voices=sep.join(voices)))

    async def _voice_change(self, ctx, args):
        if not args:
            await self.send(VOICE_CHANGE_USAGE.format(prefix=self.prefix))
            #await self.send(VOICE_CHANGE_CHECK.format(prefix=self.prefix))
            return
        
        voice_key = args.pop(0)
        success = self.seika.pick_voice(ctx.author.name, voice_key)
        if success:
            await self.send(VOICE_CHANGE_SUCCESS.format(username=ctx.author.name, voice_key=voice_key))
        else:
            await self.send(VOICE_CHANGE_FAIL.format(username=ctx.author.name, prefix=self.prefix))

        if args:
            await self._voice_speed(ctx, args)
        else:
            self.seika.save()

    async def _voice_speed(self, ctx, args):
        if not args:
            await self.send(VOICE_SPEED_USAGE.format(prefix=self.prefix))
            return

        try:
            speed = float(args.pop(0))
        except ValueError:
            await self.send(VOICE_SPEED_NAN.format(username=ctx.author.name))

        success = self.seika.pick_speed(ctx.author.name, speed)
        if success:
            await self.send(VOICE_SPEED_SUCCESS.format(username=ctx.author.name, speed=speed))
        else:
            await self.send(VOICE_SPEED_FAIL.format(username=ctx.author.name))

        if args:
            await self._voice_speed(ctx, args)
        else:
            self.seika.save()

    async def _voice_pitch(self, ctx, args):
        if not args:
            await self.send(VOICE_PITCH_USAGE.format(prefix=self.prefix))
            return

        try:
            pitch = int(args.pop(0))
        except ValueError:
            await self.send(VOICE_PITCH_NAN.format(username=ctx.author.name))
            return

        success = self.seika.pick_pitch(ctx.author.name, pitch)
        if success:
            await self.send(VOICE_PITCH_SUCCESS.format(username=ctx.author.name, pitch=pitch))
        else:
            await self.send(VOICE_PITCH_FAIL.format(username=ctx.author.name))

        if args:
            await self._voice_inton(ctx, args)
        else:
            self.seika.save()

    async def _voice_inton(self, ctx, args):
        if not args:
            await self.send(VOICE_INTON_USAGE.format(prefix=self.prefix))
            return

        try:
            inton = int(args.pop(0))
        except ValueError:
            await self.send(VOICE_INTON_NAN.format(username=ctx.author.name))
            return

        success = self.seika.pick_intonation(ctx.author.name, inton)
        if success:
            self.seika.save()
            await self.send(VOICE_INTON_SUCCESS.format(username=ctx.author.name, inton=inton))
        else:
            await self.send(VOICE_INTON_FAIL.format(username=ctx.author.name))

    async def _voice_show(self, ctx, args):
        try:
            voice_key, speed, pitch, inton = self.seika.get_params(ctx.author.name)
            await self.send(VOICE_SHOW.format(username=ctx.author.name, voice_key=voice_key, 
                speed=speed, pitch=pitch, inton=inton))
        except KeyError:
            await self.send(VOICE_SHOW_FAIL.format(username=ctx.author.name))
