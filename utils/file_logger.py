#!/usr/bin/python
import os
from logging import handlers
import json
import logging
import time
from datetime import datetime


__dir_name = os.path.abspath(__file__)
__log_path = os.path.join(__dir_name, '..', '..', 'log')
log_path = os.path.abspath(__log_path)
if not os.path.exists(log_path):
    os.mkdir(log_path)

RESERVED_ATTRS = {
    'args',
    'asctime',
    'created',
    'exc_info',
    'exc_text',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName',
}


class JSONFormatter(logging.Formatter):
    """
    A customized Python log formatter that follows our 'common log format'.

    Based on the 'logging.Formatter' class.
    """

    def __init__(self):
        super(JSONFormatter, self).__init__()

    def format(self, log_record):
        """
        Returns the resulting string after formatting.
        """
        level = log_record.levelname
        message = log_record.msg
        extra = log_record.args

        json_log_record = self.json_log_record(level, message, extra)
        return self.to_json(json_log_record)

    def to_json(self, log_record):
        """
        Convert the LogRecord into a JSON string.
        """
        return json.dumps(log_record)

    def json_log_record(self, level, message, meta_data):
        """
        Prepares a dictionary (JSON) to be logged.
        """
        log_message = {
            'log_level': level,
            'message': message,
            'timestamp': int((time.time() * 1000)),
            'ts_readable': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        log_message.update(meta_data)
        return log_message

handlers = [
    handlers.RotatingFileHandler(
        log_path + '/asterisk-agi.log',
        encoding='utf8',
        maxBytes=100000,
        backupCount=100
    ),
    logging.StreamHandler()
]

agi_file_logger = logging.getLogger()
agi_file_logger.setLevel(logging.DEBUG)

for handler in handlers:
    handler.setFormatter(JSONFormatter())
    handler.setLevel(logging.DEBUG)
    agi_file_logger.addHandler(handler)



