#!/usr/bin/vai-agi-python-path
import numpy as np
import dialplan

from scikits.audiolab import Format, Sndfile

from tempfile import mkstemp
from constants import constants
from utils import helper_functions as fn
from utils.log import __console
from fsm_interface.hermes import Hermes
from utils.read_stdin import get_stdn_var, set_agi_env, exit_AGI
from dialplan import stdin

# ================================================================
# uuid - to identify a user and the
# user's state in the state machine
host_url        = get_stdn_var(stdin.HOST)
session_id      = get_stdn_var(stdin.SESSION_ID)
client_id       = get_stdn_var(stdin.CLIENT_ID)
access_token    = get_stdn_var(stdin.ACCESS_TOKEN)
virtual_number  = get_stdn_var(stdin.VIRTUAL_NUMBER)
# - Runs a loop to read agi_ variables from stdin.
# - Creates a dict with key => agi_ variables,
#       val => agi_ var's value
env             = set_agi_env()

caller_id = env.get(dialplan.vars.AGI_CALLER_ID)

hermes = Hermes(
    host_url,
    session_id,
    client_id,
    access_token,
    caller_id,
    virtual_number,
    debug_mode=True
)
# ================================================================

def send_init():
    fsm_response = hermes\
        .hermes_configuration()

    __console.log('response: {}'.format(fsm_response))

    # Allows the dialplan program to access the variables
    # by processing FSM response
    hermes.set_variables_in_std(fsm_response)


def send_speech(file_descriptor):

    fsm_response = hermes\
        .next_action_request('AUDIO', 'FLAC', file_descriptor, conv_format='FLAC')

    __console.log('response: {}'.format(fsm_response))

    # Allows the dialplan program to access the variables
    # by processing FSM response
    hermes.set_variables_in_std(fsm_response)


def record_speech(timeout_threshold, silence_timeout_chunk, sound_array):
    merged_blocks = sound_array[:]
    _silence_ctr = 0

    while _silence_ctr <= timeout_threshold:
        raw_samples     = constants.FILE_DESCRIPTOR.read(silence_timeout_chunk)
        new_samples     = np.fromstring(raw_samples, dtype=np.int16)
        _silence_ctr    += silence_timeout_chunk

        merged_blocks = np.append(merged_blocks, new_samples)

        if not fn.is_speaking(new_samples):
            _silence_ctr = timeout_threshold + 1

    return merged_blocks


def wait_until_sound():
    _silence_ctr, samples = 0, [0]
    while fn.rms(samples) < constants.VOLUME_THRESHOLD:
        # Input Real-time Data Raw Audio from Asterisk
        raw_samples = constants.FILE_DESCRIPTOR.read(constants.CHUNK)
        samples = np.fromstring(raw_samples, dtype=np.int16)
        _silence_ctr += constants.CHUNK

        if _silence_ctr > constants.SILENCE_TIMEOUT_THRESHOLD:
            __console.log('Time Out No Speech Detected ...')
            exit_AGI()

    __console.log('Speech Detected Recording...')
    return samples


def create_flac_from(sound_samples):
    n_channels, fmt     = 1, Format('flac', 'pcm16')
    caller_id           = env[dialplan.vars.AGI_CALLER_ID]
    _, temp_sound_file  = mkstemp('TmpSpeechFile_' + caller_id + '.flac')
    flac_file           = Sndfile(temp_sound_file, 'w', fmt, n_channels, constants.RAW_RATE)

    flac_file.write_frames(np.array(sound_samples))
    return temp_sound_file


def flow_handler():
    if len(session_id) == 0:
        __console.log('launch init API')
        send_init()
    else:
        __console.log('Hello Waiting For Speech')
        sound_array = wait_until_sound()

        __console.log('Recording Speech')
        sound_samples = record_speech(
            constants.SILENCE_TIMEOUT_THRESHOLD,
            constants.SILENCE_TIMEOUT_CHUNK,
            sound_array
        )

        __console.log('Writing sound to .flac file')
        sound_file = create_flac_from(sound_samples)

        __console.log('Sending .flac file to FSM')
        send_speech(sound_file)


__console.log('loaded ', __name__)
