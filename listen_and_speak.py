#!/usr/bin/vai-agi-python-path
import traceback
from utils.log import __console
from core import core

def main():
    core.flow_handler()

try:
    __console.log('initializing listener')
    main()
except Exception as e:
    __console.err(str(e), force_print=True)
    __console.err(traceback.format_exc(), force_print=True)
