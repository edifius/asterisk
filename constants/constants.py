#!/usr/bin/python
import os


# ================================================================
# 20 s x 16000 samples/s x ( 16 bits / 8bits/byte ) = 160000 bytes
# 160000 / 1024 = +/- 157
# 157 * 1024 = 160768
#
# Default:
# TimeoutSignal = 160768
SILENCE_TIMEOUT_THRESHOLD = 43096*2

# ================================================================
# 1s x 16000 = 16000 /// This is cut in half
# 16000/1024 = 15,625 round to 16
# 16 * 1024 = 16384
# Experimental values
# Timeout_NoSpeaking=no_speak_time(RawRate * 2)
# Timeout_NoSpeaking=8046
# ================================================================
SILENCE_TIMEOUT_CHUNK   = 8192
RAW_RATE                = 8000
CHUNK                   = 1024
VOLUME_THRESHOLD        = 10000


# ================================================================
# File Descriptor delivery in Asterisk
# EAGI scripts get voice stream through file descriptor 3
FD              = 3
FILE_DESCRIPTOR = os.fdopen(FD, 'rb')
# ================================================================

# ================================================================
# File formats
# ================================================================
FLAC    = '.flac'
MP3     = '.mp3'
GSM     = '.gsm'

