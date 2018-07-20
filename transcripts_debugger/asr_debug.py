import sys
import io
from google.oauth2 import service_account
from google.cloud import speech_v1
from utils import log


class DebugTranscripts(object):
    def __init__(self, debug_mode=False, lang='en-IN'):
        self.debug_mode = debug_mode
        # ================================================================
        # This section handles speech to text for debugging purpose
        # This should not be in use if deployed
        # ================================================================
        cred_path = '/var/lib/asterisk/agi-bin/credentials_google.json'
        self.client = None
        if self.debug_mode:
            try:
                creds = service_account.Credentials \
                    .from_service_account_file(cred_path)
                self.client = speech_v1.SpeechClient(credentials=creds)
            except Exception as e:
                sys.stdout.write(str(e))

        self.lang = lang

    def debug(self, file_descriptor):
        if self.debug_mode or self.client is None:
            return None

        with io.open(file_descriptor, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech_v1.types.RecognitionAudio(content=content)
            config = speech_v1.types.RecognitionConfig(
                encoding='FLAC',
                language_code=self.lang
            )
            response = self.client.recognize(config, audio)

            for result in response.results:
                log.__console.log('Transcript: {}\n\n'.format(result.alternatives[0].transcript))

log.__console.log('loaded', __name__)