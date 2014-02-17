from __future__ import division
from elme.timer import Stopwatch
from nanpy.arduinotree import ArduinoTree
import logging
import random
import time

log = logging.getLogger(__name__)


def measure(config):
    random.seed()
    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_in = mcu.pin.get(config.pin_in)
    timer = Stopwatch()

    measurements = []
    for i in range(config.count):
            measurements.append(dict(
                                t=timer.read(),
                                Ain=p_in.read_analog_value(),
                                ))
            time.sleep(random.random() * config.max_sleep)

    data = dict(
        vcc=vcc,
        model=mcu.avr_name,
        measurements=measurements,
    )

    return data
