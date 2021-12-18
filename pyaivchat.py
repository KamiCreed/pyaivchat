import os
import argparse
from multiprocessing import Lock, Process, Queue
import subprocess
import traceback

from ytchat import YtChat
from twitchchat import TwitchChat

def start_yt(prefix, vid_id, tts_queue):
    # TODO: Search for YouTube events and allow user to pick
    ytchat = YtChat(secret_file="client_secret.json", 
            vid_id=vid_id, prefix=prefix,
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
    vid_id = os.environ['VID_ID']

    #parser = argparse.ArgumentParser(description='Twitch or YouTube chatbot and SeikaSay TTS')
    #parser.add_argument('--yt', action='store_true', help='Run YouTube chatbot instead of Twitch')
    #args = parser.parse_args()

    tts_queue = Queue()
    
    p_yt = Process(target=start_yt, args=(prefix, vid_id, tts_queue))
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
