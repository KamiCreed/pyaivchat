import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
import pickle

class YtAuth:
    vid_id = ''

    def __init__(self, secret_file, channel_id, event_type):
        self.scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        api_service_name = "youtube"
        api_version = "v3"
        self.client_secrets_file = secret_file
        self.channel_id = channel_id
        self.event_type = event_type

        def load(credentials):
             return googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials, cache_discovery=False)
        try:
            credentials = self.google_auth()
            self.youtube = load(credentials)
        except:
            # Fetch credentials if it fails
            credentials = self.google_auth(True)
            self.youtube = load(credentials)

        self.vid_id = self.get_vidid()

        self.chatid = self.get_chatid()
        print("Ready.")

    def get_vidid(self):
        request = self.youtube.search().list(
            part="snippet",
            channelId=self.channel_id,
            eventType=self.event_type,
            maxResults=1,
            order="date",
            type="video"
        )
        return request.execute()['items'][0]['id']['videoId']

    def get_chatid(self):
        print("Getting Chat ID")

        request = self.youtube.videos().list(
            part="liveStreamingDetails",
            id=self.vid_id
        )
        response = request.execute()

        return response['items'][0]['liveStreamingDetails']['activeLiveChatId']


    def google_auth(self, fetch=False):
        credentials = None
        # token.pickle stores the user's credentials from previously successful logins
        if not fetch and os.path.exists('token.pickle'):
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
                credentials = flow.run_local_server(port=0)
                with open("token.pickle", "wb") as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(credentials, f)

        return credentials

    async def send(self, msg):
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
