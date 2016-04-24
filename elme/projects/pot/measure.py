from __future__ import division

import logging
from nanpy.arduinotree import ArduinoTree
from time import sleep

from elme.timer import Stopwatch
from elme.util import avr_name
from nanpy.DigiPotX9Cxxx import DigiPot


log = logging.getLogger(__name__)


def measure(config):
    mcu = ArduinoTree()
    vcc = mcu.vcc.read()

    p_inc = mcu.pin.get(config.pin_inc)
    p_ud = mcu.pin.get(config.pin_ud)
    p_cs = mcu.pin.get(config.pin_cs)

    p_in = mcu.pin.get(config.pin_in)

    pot = DigiPot(p_inc, p_ud, p_cs)

    pot_values = range(pot.range[0], pot.range[1] + 1)
    timer = Stopwatch(len(pot_values))

    def meas():
        measurements = []
        for i in pot_values:
            pot.set(i)
            sleep(0.01)
            Ain = p_in.read_analog_value()

            measurements.append(dict(
                                t=timer.read(),
                                value=i,
                                Ain=Ain,
                                ))
            timer.next(measurements)

        return measurements

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        measurements=meas(),
    )

    return data
