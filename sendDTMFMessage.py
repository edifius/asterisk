#!/usr/bin/python
import sys
import dialplan
from fsm_interface.hermes import Hermes
from utils.log import __console
from utils.read_stdin import get_stdn_var
from dialplan import stdin
from utils.read_stdin import set_agi_env


host_url        = get_stdn_var(stdin.HOST)
session_id      = get_stdn_var(stdin.SESSION_ID)
client_id       = get_stdn_var(stdin.CLIENT_ID)
access_token    = get_stdn_var(stdin.ACCESS_TOKEN)
virtual_number  = get_stdn_var(stdin.VIRTUAL_NUMBER)
dtmf_val        = get_stdn_var(stdin.DTMF)

env = set_agi_env()

__console.log('session id = {}, dtmfval = {}'.format(session_id, dtmf_val))
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

def sendDTMF(dtmf_val):
    try:
        fsm_response = hermes.next_action_request('DTMF', None, payload=dtmf_val).json()
        __console.log('response = {}'.format(fsm_response))
        hermes.set_variables_in_std(fsm_response)

    except Exception as e:
        __console.log('Error sending dtmf', str(e))


sendDTMF(dtmf_val)

__console.log('loaded DTMF')
