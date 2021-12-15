import pytchat
import configparser
from ytchat import YtChat

def main():
    cfg = configparser.ConfigParser()
    cfg.read('./config.ini')
    vid_id = cfg.get('def', 'vid_id') # From config file
    prefix = 'k!'

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
