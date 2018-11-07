#!/usr/bin/python
import sys

def get_stdn_var(idx):
    return sys.argv[idx].strip() \
        if len(sys.argv) > idx else ''

def set_agi_env():
    env, line = {}, sys.stdin.readline().strip()
    while line != '':
        key, data = [part.strip() for part in line.split(':', 1)]
        env[key] = data
        line = sys.stdin.readline().strip()
    return env

def exit_AGI():
    sys.exit()

