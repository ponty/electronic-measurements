from __future__ import division

import logging
from nanpy.arduinotree import ArduinoTree
import time

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
    p_volt_in = mcu.pin.get(config.pin_volt_in)
    p_current_in = mcu.pin.get(config.pin_current_in)
    timer = Stopwatch()

    # max freq
#    pwm.divisor = config.pwm.divisor
#    print 'freq=%s' % pwm.frequency

    def meas():
        def loop(measurements, pwm_value):
            measurements.append(dict(
                                t=timer.read(),
                                pwm_value=pwm_value,
                                Avolt=p_volt_in.read_analog_value(),
                                Acurrent=p_current_in.read_analog_value(),
                                ))
        measurements = pwm_manager.measure(loop)

        return measurements

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        measurements=meas(),
        frequency=p_pwm.pwm.frequency,
    )

    p_pwm.reset()

    return data
