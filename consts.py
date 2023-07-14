KEY_TWITCH = 'twitch'
KEY_YOUTUBE = 'yt'
KEY_VOICE = 'voice'
VOICE_SUB = 'Usage: {prefix}voice [{keys}]'
VOICE_LS = '{username} Voices: {voices}'

VOICE_CHANGE_USAGE = 'Usage: {prefix}voice change <voice> <opt:speed> <opt:pitch> <opt:intonation>'
VOICE_CHANGE_CHECK = 'Check {prefix}voice ls to see a list of voices'
VOICE_CHANGE_SUCCESS = '{username} Voice changed to {voice_key}'
VOICE_CHANGE_FAIL = '{username} Invalid voice key. Check {prefix}voice ls'

VOICE_SPEED_USAGE = 'Usage: {prefix}voice speed <speed>'
VOICE_SPEED_NAN = '{username} Speed value is not a number'
VOICE_SPEED_SUCCESS = '{username} Voice speed changed to {speed}'
VOICE_SPEED_FAIL = '{username} Voice speed must be between 0.5 and 4.0'

VOICE_PITCH_USAGE = 'Usage: {prefix}voice pitch <pitch>'
VOICE_PITCH_NAN = '{username} Pitch value is not a number'
VOICE_PITCH_SUCCESS = '{username} Voice pitch changed to {pitch}'
VOICE_PITCH_FAIL = '{username} Voice pitch must be between 0.5 and 2.0'

VOICE_INTON_USAGE = 'Usage: {prefix}voice inton <inton>'
VOICE_INTON_NAN = '{username} Intonation value is not a number'
VOICE_INTON_SUCCESS = '{username} Voice intonation changed to {inton}'
VOICE_INTON_FAIL = '{username} Voice intonation must be between 0.0 and 2.0'

VOICE_SHOW = '{username} Voice: {voice_key}, Speed: {speed}, Pitch: {pitch}, Intonation: {inton}'
VOICE_SHOW_FAIL = '{username} You have no custom voice settings'

# TODO: Get IDs from SeikaSay2
VOICE_ID_MAP_EN = {
        'k_aoi': '5219',
        'k_akane': '5218',
        }

VOICE_ID_MAP_JP = {
        'zunda_norm': '7006',
        'zunda_ama': '7005',
        'zunda_sexy': '7007',
        'zunda_tsun': '7008',
        'mochiko': '7042',
        'tsumugi': '7009',
        }
