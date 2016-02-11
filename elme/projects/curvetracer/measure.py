from __future__ import division

import logging
from nanpy.arduinotree import ArduinoTree

from elme.pwm import PwmManager
from elme.timer import Stopwatch
from elme.util import avr_name


log = logging.getLogger(__name__)

INPUT,OUTPUT=0,1

def measure(config):
    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_pwm = mcu.pin.get(config.pin_pwm)
    pwm_manager = PwmManager(config.pwm, [p_pwm])
    p_amp = mcu.pin.get(config.pin_amp_out)
    p_in = mcu.pin.get(config.pin_x_in)
    p_out = mcu.pin.get(config.pin_x_out)
    p_rail = mcu.pin.get(config.pin_rail)
    timer = Stopwatch()

    def meas(rail):
        p_rail.write_mode(OUTPUT)
        p_rail.write_digital_value(rail)

        def loop(measurements, pwm_value):
                measurements.append(dict(
                                    t=timer.read(),
                                    pwm_value=pwm_value,
                                    Aamp=p_amp.read_analog_value(),
                                    Ain=p_in.read_analog_value(),
                                    Aout=p_out.read_analog_value(),
                                    rail=rail,
                                    ))
        measurements = pwm_manager.measure(loop)
        p_rail.reset()

        return measurements

    measurements = []
    measurements += meas(1)
    measurements += meas(0)

    p_pwm.reset()

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        pwm_frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )
    return data
