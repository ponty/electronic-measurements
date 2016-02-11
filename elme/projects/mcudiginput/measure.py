from __future__ import division

import logging
from nanpy.arduinotree import ArduinoTree
from nanpy.arduinotree import ArduinoTree

from elme.pwm import PwmManager
from elme.timer import Stopwatch
from elme.util import avr_name


log = logging.getLogger(__name__)


def measure(config):
    mcu = ArduinoTree()
#     mcu.soft_reset()

    vcc = mcu.vcc.read()
    p_pwm = mcu.pin.get(config.pin_pwm)
    pwm_manager = PwmManager(config.pwm, [p_pwm])
#    p_in = mcu.pin.get(config.pin_x_in)
#    p_out = mcu.pin.get(config.pin_x_out)
#    p_rail = mcu.pin.get(config.pin_rail)
    pin_an_in = mcu.pin.get(config.pin_an_in)
    pin_dig_in = mcu.pin.get(config.pin_dig_in)

    timer = Stopwatch()

    def meas(reverse):
        def loop(measurements, pwm_value):
                measurements.append(dict(
                                    t=timer.read(),
                                    pwm_value=pwm_value,
                                    Ain=pin_an_in.read_analog_value(),
                                    Din=pin_dig_in.read_digital_value(),
                                    reverse=reverse,
                                    ))
        measurements = pwm_manager.measure(loop, reverse=reverse)
        return measurements

    measurements = []
    measurements += meas(0)
    measurements += meas(1)

    p_pwm.reset()

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        pwm_frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )
    return data
