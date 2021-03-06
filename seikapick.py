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
    def __init__(self, tts_queue, key=KEY_TWITCH):
        self._tts_queue = tts_queue
        self.key = key

        # TODO: Get IDs from SeikaSay2
        self._voice_id_map = {
                'k_aoi': '5219',
                'k_akane': '5218',
                #'yukari': '5207',
                }

        # Default params
        self._speed = 1.0
        self._pitch = 1.3
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

        if os.path.isfile(self._json_filenames[key]):
            with open(self._json_filenames[key]) as json_file:
                self._name_maps[key] = json.load(json_file)
        else:
            self._name_maps[key] = {}

    def get_voices(self):
        return list(self._voice_id_map.keys())

    def _say(self, voice_id, speed, pitch, intonation, msg):
        self._tts_queue.put(['SeikaSay2', '-cid', str(voice_id), '-speed', str(speed), '-pitch', str(pitch), 
          '-intonation', str(intonation), '-t', msg])

    # TODO: Let users make their own voice presets
    def say_with_voice(self, username, voice_key, msg):
            voice_id = self._voice_id_map[voice_key]

    def say_for_user(self, username, msg):
        if username not in self._name_maps[self.key]:
            print("Using username as seed to choose a voice...")
            voice_key = self._pick_rand_voice(username)
            print("Voice chosen: ", voice_key)
            voice_id = self._voice_id_map[voice_key]
            speed = self._speed
            pitch = self._pitch
            intonation = self._intonation
        else:
            user_params = self._name_maps[self.key][username]
            voice_id = self._voice_id_map[self._name_maps[self.key][username][KEY_VOICE]]
            speed = user_params[KEY_SPEED] if KEY_SPEED in user_params else self._speed
            pitch = user_params[KEY_PITCH] if KEY_PITCH in user_params else self._pitch
            intonation = user_params[KEY_INTONATION] if KEY_INTONATION in user_params else self._intonation

        self._say(voice_id, speed, pitch, intonation, msg)

    def _pick_rand_voice(self, username):
        self.user_rand.seed(username) # Pick random voice, but be the same for their user
        voice_key = self.user_rand.choice(list(self._voice_id_map.keys()))
        return voice_key

    def pick_voice(self, username, voice_key):
        if voice_key not in self._voice_id_map:
            return False
        self._name_maps[self.key][username] = {}
        self._name_maps[self.key][username][KEY_VOICE] = voice_key
        return True

    def _give_voice_if_needed(self, username):
        if username not in self._name_maps[self.key]:
            self._name_maps[self.key][username] = {}
            self._name_maps[self.key][username][KEY_VOICE] = self._pick_rand_voice(username)

    def pick_speed(self, username, speed):
        if speed > 4 or speed < 0.5:
            return False
        self._give_voice_if_needed(username)
        self._name_maps[self.key][username][KEY_SPEED] = speed
        return True

    def pick_pitch(self, username, pitch):
        if pitch > 2 or pitch < 0.5:
            return False
        self._give_voice_if_needed(username)
        self._name_maps[self.key][username][KEY_PITCH] = pitch
        return True

    def pick_intonation(self, username, intonation):
        if intonation > 2 or intonation < 0:
            return False
        self._give_voice_if_needed(username)
        self._name_maps[self.key][username][KEY_INTONATION] = intonation
        return True

    def get_params(self, username):
        # Raises KeyError exception
        user_params = self._name_maps[self.key][username]
        voice_id = user_params[KEY_VOICE]
        speed = user_params[KEY_SPEED] if KEY_SPEED in user_params else self._speed
        pitch = user_params[KEY_PITCH] if KEY_PITCH in user_params else self._pitch
        intonation = user_params[KEY_INTONATION] if KEY_INTONATION in user_params else self._intonation

        return voice_id, speed, pitch, intonation

    def save(self):
        # Save corresponding JSON file
        self._save_json(self._name_maps[self.key], self._json_filenames[self.key])

    @staticmethod
    def _save_json(name_map, filename):
        with open(filename, 'w') as out:
            json.dump(name_map, out)
