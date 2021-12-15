import pytchat

import os
import configparser

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pickle

class YtChat:
    def __init__(self, secret_file, vid_id):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self.scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        api_service_name = "youtube"
        api_version = "v3"
        self.client_secrets_file = secret_file
        self.vid_id = vid_id

        credentials = self.google_auth()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.chatid = self.get_chatid()
        print("Ready.")

    def get_chatid(self):
        print("Getting Chat ID")
        request = self.youtube.videos().list(
            part="liveStreamingDetails",
            id=self.vid_id
        )
        response = request.execute()

        return response['items'][0]['liveStreamingDetails']['activeLiveChatId']


    def google_auth(self):
        credentials = None
        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists('token.pickle'):
            print('Loading Credentials From File...')
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refreshing Access Token...')
                credentials.refresh(Request())
            else:
                print('Fetching New Tokens...')

                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes)
                credentials = flow.run_console()
                with open("token.pickle", "wb") as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(credentials, f)

        return credentials

    def send_message(self, msg):
        print("Sending message: ", msg)
        request = self.youtube.liveChatMessages().insert(
            part="snippet",
            body={
              "snippet": {
                "liveChatId": self.chatid,
                "type": "textMessageEvent",
                "textMessageDetails": {
                  "messageText": msg
                }
              }
            }
        )
        response = request.execute()

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
