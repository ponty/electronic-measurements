from __future__ import division
from numpy.core.function_base import logspace
from numpy.ma.core import log10
from softusbduino import Arduino
from softusbduino.const import OUTPUT
from elme.timer import Stopwatch
from elme.util import sleep_and_read


INVERT = 1


def measure(config):
    mcu = Arduino()
    mcu.pins.reset()
    vcc = mcu.vcc.voltage
    p_middle = mcu.pin(config.pin_middle)
#    if config.pullup:
#        assert INVERT
#    p_middle.write_pullup(config.pullup)

    timer = Stopwatch()

    def measure1(p_pwm, R, frequency):
        measurements = []

        if INVERT:
            Abottom = 1023
            top = 0
            Atop = 0
        else:
            Abottom = 0
            top = 1
            Atop = 1023

#        pin_rail.write_mode(OUTPUT)
#        pin_rail.write_digital_out(top)
        p_pwm.write_mode(OUTPUT)
        p_pwm.pwm.set_high_freq_around(frequency)
        frequency = p_pwm.pwm.read_frequency()

        sleep_and_read(config.settle_time, p_middle)

        for _ in range(config.window):
            Amiddle = p_middle.read_analog()
            measurements.append(dict(
                                t=timer.read(),
                                Amiddle=Amiddle,
                                R=R,
                                frequency=frequency,
                                ))
#        if pin_input:
#            for _ in range(config.filter_size):
#                Atop = pin_input.read_analog()
#                measurements.append(dict(
#                                    t=timer.read(),
#                                    R=R,
#                                    Atop=Atop,
#                                    ))
#        else:
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
        p_pwm.reset()
        return measurements

    measurements = []
    for d in config.toplist:
        p_pwm = mcu.pin(d['pin_pwm'])

#        pin_input = None
#        if 'pin_input' in d:
#            pin_input = mcu.pin(d['pin_input'])

        R = d['R']
        for f in logspace(log10(config.freq.min), log10(config.freq.max), config.freq.steps):
            measurements += measure1(p_pwm, R, f)

    data = dict(
        vcc=vcc,
        model=mcu.model,
        measurements=measurements,
    )

    return data
