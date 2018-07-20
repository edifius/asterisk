import sys
import dialplan

# ================================================================
# EAGI or AGI do not show print statements,
# this wrapper writes to the stdout or stderr
# which is even read by the dialplan,
# so variables can be set/reset/manipulated etc.
class AGIConsole(object):
    def __init__(self, debug_mode=True):
        self.debug_mode = debug_mode

    def __console_base(self, log_type, command, action, *args, **kwargs):
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
