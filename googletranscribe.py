#! /usr/bin/python
from collections import namedtuple
from contextlib import closing
from asterisk.agi import *
import time
import os
import io
import wave
import audioop
import base64
import json
# Imports the Google Cloud client library
from google.cloud import speech
# import speech_recognition as sr
from time import sleep
from tempfile import gettempdir, mkstemp

from google.cloud.speech import enums
from google.cloud.speech import types

from google.oauth2 import service_account

# Instantiates a client
credentials = service_account.Credentials.from_service_account_file("/etc/asterisk/eagi/cred.json")
speech_client = speech.SpeechClient(credentials=credentials)
agi = AGI()
agi.verbose("Google transcribe script started..")
ani = agi.env['agi_callerid']
did = agi.env['agi_extension']
agi.answer()
agi.verbose("call answered from : %s to %s" % (ani, did))

time.sleep(10)

agi.verbose("Waited ten seconds, now sending file.")
try:
    with io.open(3, 'rb') as audio_file:
        content = audio_file.read(102400)
        agi.verbose("The content has been written to")
except Exception as e:
    agi.verbose("There was a problem opening the file: " + str(e))

stream = [content]
requests = (types.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in stream)

config = types.RecognitionConfig(
encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
sample_rate_hertz=16000,
language_code='en-US')

streaming_config = types.StreamingRecognitionConfig(config=config)

# streaming_recognize returns a generator
# Start migration_streaming_response
responses = speech_client.streaming_recognize(streaming_config, requests)
# Detects speech in the audio file

agi.verbose("Responses : {}".format(responses))

for response in responses:
    agi.verbose("Response: {}".format(response))
    for result in response.results:
        agi.verbose('Finished: {}'.format(results.is_final))
        agi.verbose('Stability: {}'.format(results.stability))
        alternatives = result.alternatives
        for alternative in alternatives:
            agi.verbose('Confidence: {}'.format(alternative.confidence))
            agi.verbose(u'Transcript: {}'.format(alternative.transcript))

agi.verbose("Google transcription complete")
agi.hangup()
#exit()