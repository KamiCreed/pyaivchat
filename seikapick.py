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
        self._voice_id_map = {
                'k_aoi': '5219',
                'k_akane': '5218',
                #'yukari': '5207',
                }

        # Default params
        self._speed = 1.2
        self._pitch = 1.1
        self._intonation = 1.0


        self._json_filenames = {
                KEY_TWITCH: 'twitch_name_map.json',
                KEY_YOUTUBE: 'youtube_name_map.json',
                }

        self._name_maps = {
                KEY_TWITCH: {},
                KEY_YOUTUBE: {},
                }

        for key, name_map in self._name_maps.items():
            if os.path.isfile(self._json_filenames[key]):
                with open(self._json_filenames[key]) as json_file:
                    self._name_maps[key] = json.load(json_file)
            else:
                self._name_maps[key] = {}

    def get_voices(self):
        return list(self._voice_id_map.keys())

    @staticmethod
    def _say(voice_id, speed, pitch, intonation, msg):
        subprocess.run(['SeikaSay2', '-cid', str(voice_id), '-speed', str(speed), '-pitch', str(pitch), 
          '-intonation', str(intonation), '-t', msg])

    def say_for_user(self, username, msg, key=KEY_TWITCH):
        if username not in self._name_maps[key]:
            print("Randomly choosing a name for new user...")
            voice_key = random.choice(list(self._voice_id_map.keys())) # Pick a random voice
            self._pick_voice(username, voice_key, key) # Pick a random voice
            print("Voice chosen: ", voice_key)

        speed = self._name_maps[key][username][KEY_SPEED] if KEY_SPEED in self._name_maps[key][username] else self._speed
        pitch = self._name_maps[key][username][KEY_PITCH] if KEY_PITCH in self._name_maps[key][username] else self._pitch
        intonation = self._name_maps[key][username][KEY_INTONATION] if KEY_INTONATION in self._name_maps[key][username] else self._intonation
        voice_id = self._voice_id_map[self._name_maps[key][username][KEY_VOICE]]
        self._say(voice_id, speed, pitch, intonation, msg)

    def _pick_voice(self, username, voice_id, key=KEY_TWITCH):
        self._name_maps[key][username] = {}
        self._name_maps[key][username][KEY_VOICE] = voice_id
        self._save_json(self._name_maps[key], self._json_filenames[key])

    @staticmethod
    def _save_json(name_map, filename):
        with open(filename, 'w') as out:
            json.dump(name_map, out)
