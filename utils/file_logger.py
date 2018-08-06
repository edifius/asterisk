#!/usr/bin/vai-agi-python-path
import os
import logging
from logging import handlers


__dir_name = os.path.abspath(__file__)
__log_path = os.path.join(__dir_name, '..', '..', 'log')
log_path = os.path.abspath(__log_path)
if not os.path.exists(log_path):
    os.mkdir(log_path)


format = logging.Formatter(
    fmt='%(levelname)s:[%(asctime)s](%(filename)s:%(lineno)d): %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

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
    handler.setFormatter(format)
    handler.setLevel(logging.DEBUG)
    agi_file_logger.addHandler(handler)
