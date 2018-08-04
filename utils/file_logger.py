import logging
from logging import handlers

format = logging.Formatter(
    fmt='%(levelname)s:[%(asctime)s](%(filename)s:%(lineno)d): %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

handlers = [
    handlers.RotatingFileHandler(
        'asterisk-agi.log',
        encoding='utf8',
        maxBytes=100000,
        backupCount=100
    ),
    logging.StreamHandler()
]

agi_logger = logging.getLogger()
agi_logger.setLevel(logging.DEBUG)

for handler in handlers:
    handler.setFormatter(format)
    handler.setLevel(logging.DEBUG)
    agi_logger.addHandler(handler)

agi_logger.info('yo boi')