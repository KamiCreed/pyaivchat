import subprocess
import json
import os
import random
import copy

from consts import *

KEY_VOICE = 'voice_key'
KEY_SPEED = 'speed'
KEY_PITCH = 'pitch'
KEY_INTONATION = 'intonation'

class SeikaPick:
    def __init__(self):
        self.voice_id_map = {
                'k_aoi': '5219',
                'k_akane': '5218',
                #'yukari': '5207',
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

    def say(self, voice_id, speed, pitch, intonation, msg):
        subprocess.run(['SeikaSay2', '-cid', str(voice_id), '-speed', str(speed), '-pitch', str(pitch), 
          '-intonation', str(intonation), '-t', msg])

    def say_for_user(self, username, msg, key=KEY_TWITCH):
        if username not in self.name_maps[key]:
            self.pick_voice(username, random.choice(list(self.voice_id_map.keys())), key) # Pick a random voice
        speed = self.name_maps[key][username][KEY_SPEED] if KEY_SPEED in self.name_maps[key][username] else self.speed
        pitch = self.name_maps[key][username][KEY_PITCH] if KEY_PITCH in self.name_maps[key][username] else self.pitch
        intonation = self.name_maps[key][username][KEY_INTONATION] if KEY_INTONATION in self.name_maps[key][username] else self.intonation
        voice_id = self.voice_id_map[self.name_maps[key][username][KEY_VOICE]]
        self.say(voice_id, speed, pitch, intonation, msg)

    def pick_voice(self, username, voice_id, key=KEY_TWITCH):
        self.name_maps[key][username] = {}
        self.name_maps[key][username][KEY_VOICE] = voice_id
        self.save_json(self.name_maps[key], self.json_filenames[key])

    def save_json(self, name_map, filename):
        with open(filename, 'w') as out:
            json.dump(name_map, out)
