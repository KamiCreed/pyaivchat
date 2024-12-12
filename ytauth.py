import os
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
import pickle

class YtAuth:
    MAX_WAIT_SEC = 120
    WAIT_BASE = 2

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

        self.vid_ids = self._get_vidids()

        self.chatid_map = self._get_chatids()
        print("Ready.")

    def _build_request(self, event_type):
        return self.youtube.search().list(
            part="snippet",
            channelId=self.channel_id,
            eventType=event_type,
            maxResults=2,
            order="date",
            type="video"
        )

    def _get_vidids(self):
        live_event_type = "live"
        upcoming_event_type = "upcoming"

        request = self._build_request(live_event_type)
        response = request.execute()
        if not response['items']:
            # Assume not currently live
            request = self._build_request(upcoming_event_type)
            response = request.execute()

        incidents = 0
        while not response['items']:
            wait_sec = self.WAIT_BASE**incidents
            print("Bad response. Waiting for", wait_sec, "seconds...")
            time.sleep(wait_sec)
            response = request.execute()
            incidents += 1
            if wait_sec > self.MAX_WAIT_SEC:
                # Oscillate wait time
                incidents = 0

        videoIds = []
        for item in response['items']:
            videoIds.append(item['id']['videoId'])

        return videoIds

    def _get_chatids(self):
        print("Getting Chat ID")

        chat_id_map = {}
        for vid_id in self.vid_ids:
            request = self.youtube.videos().list(
                part="liveStreamingDetails",
                id=vid_id
            )
            response = request.execute()
            chat_id_map[vid_id] = response['items'][0]['liveStreamingDetails']['activeLiveChatId']

        return chat_id_map


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

    async def send(self, msg, vid_id):
        chatid = self.chatid_map[vid_id]

        print("Sending message: ", msg)
        request = self.youtube.liveChatMessages().insert(
            part="snippet",
            body={
              "snippet": {
                "liveChatId": chatid,
                "type": "textMessageEvent",
                "textMessageDetails": {
                  "messageText": msg
                }
              }
            }
        )
        response = request.execute()
