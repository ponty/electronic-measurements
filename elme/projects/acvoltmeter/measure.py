from __future__ import division

import logging
from nanpy.arduinotree import ArduinoTree
import random
import time

from elme.timer import Stopwatch
from elme.util import avr_name


log = logging.getLogger(__name__)


def measure(config):
    random.seed()
    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_in = mcu.pin.get(config.pin_in)
    timer = Stopwatch(config.count)

    measurements = []
    for i in range(config.count):
            measurements.append(dict(
                                t=timer.read(),
                                Ain=p_in.read_analog_value(),
                                ))
            time.sleep(random.random() * config.max_sleep)
            timer.next(measurements)

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        measurements=measurements,
    )

    return data
