import subprocess
import json
import os
import random

from consts import *

class SeikaPick:
    def __init__(self):
        self.voice_id_map = {
                'k_aoi': 5219,
                'k_akane': 5218,
                #'yukari': 5207,
                }

        # Default params
        self.speed = 1.2
        self.pitch = 1.1
        self.intonation = 1.0


        self.json_filenames = {
                KEY_TWITCH: 'twitch_name_map.json',
                KEY_YOUTUBE: 'youtube_name_map.json',
                }

        self.name_maps = {
                KEY_TWITCH: {},
                KEY_YOUTUBE: {},
                }

        for key, name_map in self.name_maps.items():
            if os.path.isfile(self.json_filenames[key]):
                with open(self.json_filenames[key]) as json_file:
                    name_map = json.load(json_file)
            else:
                name_map = {}

    def say(self, voice_id, msg):
        subprocess.run(['SeikaSay2', '-cid', voice_id, '-t', msg])

    def say_for_user(self, username, msg, key=KEY_TWITCH):
        if username not in self.name_maps[key]:
            self.pick_voice(username, random.choice([self.voice_id_map.keys()]), key) # Pick a random voice
        voice_id = self.voice_id_map[self.name_maps[key][username]]
        self.say(self.voice_id_map[voice_id], msg)

    def pick_voice(self, username, voice_id, key=KEY_TWITCH):
        self.name_maps[key][username] = voice_id
        self.save_json(self.name_maps[key], self.json_filenames[key])

    def save_json(self, name_map, filename):
        with open(filename, 'w') as out:
            json.dump(name_map, out)
