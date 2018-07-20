#!/usr/bin/python
import traceback
from utils.log import __console
from core import core

def main():
    core.flow_handler()
try:
    main()
except Exception as e:
    __console.log(str(e), force_print=True)
    __console.log(traceback.format_exc(), force_print=True)
