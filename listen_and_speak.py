#!/usr/bin/python

import traceback
import signal
from utils.log import __console
from core import core
import dialplan


def capture_user_hangup(signum, frame):
    __console.log('captured', signum)

signal.signal(signal.SIGHUP, capture_user_hangup)

try:
    __console.log('initializing listener')
    core.flow_handler()
except Exception as e:
    __console.err(str(e), force_print=True)
    __console.err(traceback.format_exc(), force_print=True)
    __console.set_var(dialplan.vars.CALL_ACTUAL_PHONE, 'true')
