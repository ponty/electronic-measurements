from __future__ import division

from nanpy.arduinotree import ArduinoTree
from nanpy.arduinotree import ArduinoTree
import time

from elme.timer import Stopwatch
from elme.util import avr_name


# Test:
# R=1M
# INVERT=0    Arail=1021-1022
# INVERT=1    Arail=0  -> better
INVERT = 1

INPUT,OUTPUT=0,1


def measure(config):
    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_middle = mcu.pin.get(config.pin_middle)
    if config.pullup:
        assert INVERT
    p_middle.write_pullup(config.pullup)
    # p_bottom = mcu.pin.get(config.pin_bottom)

    timer = Stopwatch()

    def measure1(pin_rail, pin_input, R):
        measurements = []

        if INVERT:
            Abottom = 1023
            top = 0
            Atop = 0
        else:
            Abottom = 0
            top = 1
            Atop = 1023
#        Abottom = 0

#        p_bottom.mode =
        pin_rail.write_mode(OUTPUT)
#        p_bottom.write_digital_value(bottom)
        pin_rail.write_digital_value(top)

        # first read is not stable by 1MOhm because of A/D capacitor
        p_middle.read_analog_value()
        p_middle.read_analog_value()
        p_middle.read_analog_value()

        time.sleep(0.02)

        for _ in range(config.window):
            Amiddle = p_middle.read_analog_value()
            measurements.append(dict(
                                t=timer.read(),
                                Amiddle=Amiddle,
                                R=R,
                                ))
        if pin_input:
            for _ in range(config.window):
                Atop = pin_input.read_analog_value()
                measurements.append(dict(
                                    t=timer.read(),
                                    R=R,
                                    Atop=Atop,
                                    ))
        else:
            measurements.append(dict(
                                t=timer.read(),
                                R=R,
                                Atop=Atop,
                                ))
        measurements.append(dict(
            t=timer.read(),
            Abottom=Abottom,
            R=R,
        ))
        # p_bottom.reset()
        pin_rail.reset()
        return measurements

    measurements = []
    for d in config.toplist:
        pin_rail = mcu.pin.get(d['pin_rail'])

        pin_input = None
        if 'pin_input' in d:
            pin_input = mcu.pin.get(d['pin_input'])

        R = d['R']
        measurements += measure1(pin_rail, pin_input, R)
#        measurements += measure1(pin_rail, pin_input,R, 1)

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        measurements=measurements,
    )

    return data
