#!/usr/bin/vai-agi-python-path
from agi_logger import AGIConsole
from utils import sys_vars


logging_meta_data = {
    'host_url'        : sys_vars.host_url,
    'session_id'      : sys_vars.session_id,
    'client_id'       : sys_vars.client_id,
    'access_token'    : sys_vars.access_token,
    'virtual_number'  : sys_vars.virtual_number,
    'caller_id'       : sys_vars.caller_id,
    'env'             : sys_vars.env
}

__console = AGIConsole(debug_mode=True, meta_data=logging_meta_data)
