import subprocess
import json
import os
from random import Random
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

        self.user_rand = Random() # Used to keep the same voice for new users

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
            print("Using username as seed to choose a voice...")
            voice_key = self._pick_rand_voice(username)
            print("Voice chosen: ", voice_key)
            voice_id = self._voice_id_map[voice_key]
        else:
            voice_id = self._voice_id_map[self._name_maps[key][username][KEY_VOICE]]

        speed = self._name_maps[key][username][KEY_SPEED] if KEY_SPEED in self._name_maps[key][username] else self._speed
        pitch = self._name_maps[key][username][KEY_PITCH] if KEY_PITCH in self._name_maps[key][username] else self._pitch
        intonation = self._name_maps[key][username][KEY_INTONATION] if KEY_INTONATION in self._name_maps[key][username] else self._intonation
        self._say(voice_id, speed, pitch, intonation, msg)

    def _pick_rand_voice(self, username):
        self.user_rand.seed(username) # Pick random voice, but be the same for their user
        voice_key = self.user_rand.choice(list(self._voice_id_map.keys()))
        return voice_key

    def pick_voice(self, username, voice_key, key=KEY_TWITCH):
        if voice_key not in self._voice_id_map:
            return False
        self._name_maps[key][username] = {}
        self._name_maps[key][username][KEY_VOICE] = voice_key
        return True

    def _give_voice_if_needed(self, username, key=KEY_TWITCH
        if username not in self._name_maps[key]:
            self._name_maps[key][username] = {}
            self._name_maps[key][username][KEY_VOICE] = self._pick_rand_voice(username)

    def pick_speed(self, username, speed, key=KEY_TWITCH):
        if speed > 4 or speed < 0.5:
            return False
        self._give_voice_if_needed(username, key)
        self._name_maps[key][username][KEY_SPEED] = speed
        return True

    def pick_pitch(self, username, pitch, key=KEY_TWITCH):
        if pitch > 2 or pitch < 0.5:
            return False
        self._give_voice_if_needed(username, key)
        self._name_maps[key][username][KEY_PITCH] = speed
        return True

    def pick_intonation(self, username, intonation, key=KEY_TWITCH):
        if intonation > 2 or intonation < 0:
            return False
        self._give_voice_if_needed(username, key)
        self._name_maps[key][username][KEY_INTONATION] = speed
        return True

    def save(self, key=KEY_TWITCH):
        # Save corresponding JSON file
        self._save_json(self._name_maps[key], self._json_filenames[key])

    @staticmethod
    def _save_json(name_map, filename):
        with open(filename, 'w') as out:
            json.dump(name_map, out)
