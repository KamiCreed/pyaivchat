import os
import argparse
from multiprocessing import Lock, Process, Queue
import subprocess
import traceback

from ytauth import YtAuth
from ytchat import YtChat
from twitchchat import TwitchChat

SECRET_FILE = 'client_secret.json'

def start_yt(prefix, tts_queue, ytauth):
    # TODO: Search for YouTube events and allow user to pick
    ytchat = YtChat(secret_file=SECRET_FILE,
            vid_id=ytauth.vid_id, prefix=prefix,
            ytauth=ytauth,
            tts_queue=tts_queue)
    ytchat.run()

def start_twitch(prefix, tts_queue):
    bot = TwitchChat(
        # set up the bot
        token=os.environ['TOKEN'],
        prefix=prefix,
        tts_queue=tts_queue,
        initial_channels=[os.environ['CHANNEL']]
    )
    bot.run()

def send_say_requests(tts_queue):
    while True:
        try:
            cmd = tts_queue.get(block=True)
            subprocess.run(cmd)
        except Exception:
            traceback.print_exc()
            print("Ignoring exception for tts commands...")

def main():
    prefix = os.environ['BOT_PREFIX']
    channel_id = os.environ['CHANNEL_ID']
    event_type = os.environ['EVENT_TYPE']

    parser = argparse.ArgumentParser(description='Twitch and YouTube chatbot using SeikaSay TTS')
    parser.add_argument('--no-yt', action='store_true', help='Disable YouTube bot')
    parser.add_argument('--no-tw', action='store_true', help='Disable Twitch bot')
    args = parser.parse_args()

    tts_queue = Queue()
    
    auth = YtAuth(SECRET_FILE, channel_id, event_type)
    p_yt = Process(target=start_yt, args=(prefix, tts_queue, auth))
    p_tw = Process(target=start_twitch, args=(prefix, tts_queue))
    p_yt.start()
    p_tw.start()

    # Send TTS requests
    send_say_requests(tts_queue)

    p_yt.join()
    p_tw.join()
    #if args.yt:
    #    start_yt(prefix, vid_id)
    #else:
    #    start_twitch(prefix)

    print("End.")


if __name__ == "__main__":
    main()
