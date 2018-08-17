#!/usr/bin/vai-agi-python-path
import numpy as np
from constants import constants
from utils.log import __console

rms         = lambda samples: np.sqrt(np.mean(np.square(samples))) * 1000
is_speaking = lambda data: rms(data) > constants.VOLUME_THRESHOLD

get_silence_timeout_chunk   = lambda rate: 1024 * int(np.rint(rate / 1024))
timeout_gen                 = lambda x, rate: 1024 * int(np.rint((x * rate)/1024))
