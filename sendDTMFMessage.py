#!/usr/bin/python
from fsm_interface.hermes import Hermes
from utils.log import __console
from utils.read_stdin import set_agi_env
from utils import sys_vars


host_url        = sys_vars.host_url
session_id      = sys_vars.session_id
client_id       = sys_vars.client_id
access_token    = sys_vars.access_token
virtual_number  = sys_vars.virtual_number
caller_id       = sys_vars.caller_id
dtmf_val        = sys_vars.dtmf


env = set_agi_env()
__console.log('session id = {}, dtmfval = {}'.format(session_id, dtmf_val))

hermes = Hermes(
    host_url,
    session_id,
    client_id,
    access_token,
    caller_id,
    virtual_number,
    debug_mode=True
)

def sendDTMF(dtmf_val):
    try:
        fsm_response = hermes.next_action_request('DTMF', None, payload=dtmf_val).json()
        __console.log('response = {}'.format(fsm_response))
        hermes.set_variables_in_std(fsm_response)

    except Exception as e:
        __console.log('Error sending dtmf', str(e))


sendDTMF(dtmf_val)

__console.log('loaded DTMF')
