#!/usr/bin/vai-agi-python-path
import uuid
import requests

import dialplan
from utils.agi_logger import AGIConsole
from utils import file_handler
from utils.log import __console
from utils.retry_api_call import requests_retry_session

def create_hermes_headers(access_token, caller_number, call_id, virtual_number):
    return {
        'X-ACCESS-TOKEN': access_token, # "2f4a148510e14e457b50461260c4cb05",
        'CALLER-NUMBER': caller_number,
        'CALL-UUID': call_id,
        'VIRTUAL-NUMBER': virtual_number,
        'Cache-Control': "no-cache",
    }


class Hermes(object):
    def __init__(
        self,
        host,
        session_id,
        client_id,
        access_token,
        caller_number,
        virtual_number,
        debug_mode=False,
        **kwargs
    ):
        self.__console = AGIConsole(debug_mode=debug_mode, meta_data={
            'host_url'          : host,
            'session_id'        : session_id,
            'client_id'         : client_id,
            'access_token'      : access_token,
            'virtual_number'    : virtual_number,
            'caller_id'         : caller_number,
            'dtmf'              : None,
            'env'               : None
        })
        caller_number = caller_number if caller_number is not None else '+8197954499'
        call_id = uuid.uuid4().hex if session_id == '' else session_id
        if session_id == '':
            self.__console.set_var(dialplan.vars.SESSION_ID, call_id)

        headers = create_hermes_headers(access_token, caller_number, call_id, virtual_number)
        self.headers = headers.copy()
        self.headers.update(kwargs)

        self.client = client_id
        self.host = host
        self.url = ''

    def update_url(self, url):
        self.url = self.host + url.format(client=self.client)

    def hermes_configuration(self, **kwargs):
        """
        Fetch client configuration
        :returns: Configuration with next action defaults
        """
        self.update_url('/api/{client}/configuration/')
        response = requests_retry_session().get(self.url, headers=self.headers, params=kwargs)
        self.__console.log('Configuration api response', **{
            'url': self.url,
            'headers': self.headers,
            'response_text': str(response.text),
            'response_status_code': str(response.status_code)
        })
        try:
            return response.json()
        except Exception as e:
            self.__console.log('Response error', str(e))


    def next_action_request(self, payload_type, audio_format, payload, conv_format=None):
        """
        Send audio/DTMF payload to `hermes`
        :param payload_type: Can be `AUDIO` or `DTMF`
        :param payload: Audio file path or DTMF value
        :param client: Name of the client as registered with Vernacular
        :returns: Next action details
        """
        # ======================================================
        # Set the url to obtain the next action, playback file name
        self.update_url('/api/{client}/call_flow/')

        self.__console.log('url = {}'.format(self.url))
        self.__console.log('headers = {}'.format(self.headers))

        if payload_type == 'AUDIO':
            data = {
                'payload_type': payload_type,
                'audio_format': audio_format,
                'audio_conversion_format': conv_format
            }
            file_data = {'payload': open(payload, 'rb')}
            response = requests_retry_session().post(self.url, data=data, files=file_data, headers=self.headers)
            self.__console.log('call flow audio response', **{
                'url': self.url,
                'headers': self.headers,
                'response_text': str(response.text),
                'response_status_code': str(response.status_code)
            })
            return response.json()

        elif payload_type == 'DTMF':
            data = {'payload_type': payload_type, 'payload': payload}
            response = requests_retry_session().post(self.url, data=data, headers=self.headers)
            self.__console.log('call flow dtmf response', **{
                'url': self.url,
                'headers': self.headers,
                'response_text': str(response.text),
                'response_status_code': str(response.status_code)
            })
            return response.json()

    def get_params_from(self, fsm_response):
        self.__console.log('response {}'.format(fsm_response))

        response_action             = fsm_response.get('action')
        response_action_expected    = response_action.get('type')
        resource_url                = response_action.get('resource')
        resource_name               = resource_url.split('/')[-1]
        resource_name_gsm           = resource_name.replace('.mp3', '')

        return resource_url, response_action_expected, resource_name_gsm

    def set_variables_in_std(self, fsm_response):
        resource_url, next_action, resource_name_gsm = self.get_params_from(fsm_response)
        # ========================================================================
        # PLAY_FILE is the name of the file to be streamed to a caller
        # ========================================================================
        file_path = file_handler.download(resource_url)
        self.__console.set_var(dialplan.vars.PLAY_FILE, file_path)
        # ========================================================================
        # Extra actions apart from the PLAY_FILE that have to be performed,
        # are set here for the dialplan to use.
        #
        # Any value is suitable for the variables as long as it is a string
        # 'true' is chosen for semantics, the dialplan checks for <var> != ''
        # for the extra actions.
        # ========================================================================
        action_state = 'true'
        action_set = {
            'HANGUP': (dialplan.vars.TERMINATE, action_state),
            'DTMF': (dialplan.vars.READ_DTMF, action_state),
            'TRANSFER': (dialplan.vars.CALL_ACTUAL_PHONE, action_state)
        }
        if next_action in action_set:
            self.__console.log(*action_set[next_action])
            self.__console.set_var(*action_set[next_action])

__console.log('loaded ', __name__)
