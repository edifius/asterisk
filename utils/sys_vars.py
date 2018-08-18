#!/usr/bin/python
from utils.read_stdin import get_stdn_var, set_agi_env
from dialplan import stdin


# ================================================================
# uuid - to identify a user and the
# user's state in the state machine
host_url        = get_stdn_var(stdin.HOST)
session_id      = get_stdn_var(stdin.SESSION_ID)
client_id       = get_stdn_var(stdin.CLIENT_ID)
access_token    = get_stdn_var(stdin.ACCESS_TOKEN)
virtual_number  = get_stdn_var(stdin.VIRTUAL_NUMBER)
caller_id       = get_stdn_var(stdin.CALLER_ID)
dtmf            = get_stdn_var(stdin.DTMF)

# - Runs a loop to read agi_ variables from stdin.
# - Creates a dict with key => agi_ variables,
#       val => agi_ var's value
env             = set_agi_env()
