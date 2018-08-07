#!/usr/bin/vai-agi-python-path
import sys
import dialplan
from inspect import getframeinfo, stack
from file_logger import agi_file_logger


# ================================================================
# EAGI or AGI do not show print statements,
# this wrapper writes to the stdout or stderr
# which is even read by the dialplan,
# so variables can be set/reset/manipulated etc.
class AGIConsole(object):
    def __init__(self, debug_mode=True, meta_data=None):
        self.debug_mode = debug_mode
        self.meta_data = meta_data

    def __console_base(self, log_type, command, action, *args, **kwargs):
        caller = getframeinfo(stack()[1][0])
        force_print = 'force_print' in kwargs and kwargs['force_print']
        if not force_print and\
            not self.debug_mode and\
            command == dialplan.commands.EXEC and\
            action == dialplan.actions.NOOP:
            return

        if log_type not in ['stdout', 'stderr']:
            log_type = 'stdout'

        args_list_stringified = ', '.join([str(arg) for arg in args])\
            if args is not None else ''

        __stdwriter = getattr(sys, log_type)

        payload = '{command} "{action}" "{args_list_stringified}"\n'.format(
            command=command,
            action=action,
            args_list_stringified=args_list_stringified
        )

        file_log_payload = {
            'caller_number'         : self.meta_data.get('caller_id') if self.meta_data is not None else 'NA',
            'virtual_number'        : self.meta_data.get('virtual_number') if self.meta_data is not None else 'NA',
            'access_token'          : self.meta_data.get('access_token') if self.meta_data is not None else 'NA',
            'client_id'             : self.meta_data.get('client_id') if self.meta_data is not None else 'NA',
            'host_url'              : self.meta_data.get('base_url') if self.meta_data is not None else 'NA',
            'session_id'            : self.meta_data.get('session_id') if self.meta_data is not None else 'NA',
            'dtmf'                  : self.meta_data.get('dtmf') if self.meta_data is not None else 'NA',
            'url'                   : 'NA',
            'headers'               : 'NA',
            'response_text'         : 'NA',
            'response_status_code'  : 'NA'
        }

        if len(kwargs):
            file_log_payload.update(kwargs)


        agi_file_logger.error(args_list_stringified, file_log_payload)\
            if log_type == 'stderr'\
            else agi_file_logger.info(args_list_stringified, file_log_payload)

        __stdwriter.write(payload)
        __stdwriter.flush()

    def console_log(self, command, action, *args, **kwargs):
        self.__console_base('stdout', command, action, *args, **kwargs)

    def console_err(self, command, action, *args, **kwargs):
        self.__console_base('stderr', command, action, *args, **kwargs)

    def log(self, *args, **kwargs):
        self.console_log(dialplan.commands.EXEC, dialplan.actions.NOOP, *args, **kwargs)

    def err(self, *args, **kwargs):
        self.console_err(dialplan.commands.EXEC, dialplan.actions.NOOP, *args, **kwargs)

    def set_var(self, key, value):
        self.console_log(dialplan.commands.SET_VARIABLE, key, value)
