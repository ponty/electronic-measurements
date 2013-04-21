from __future__ import division
from softusbduino import Arduino
from elme.pwm import PwmManager
from elme.timer import Stopwatch
import logging

log = logging.getLogger(__name__)


def measure(config):
    mcu = Arduino()
    mcu.pins.reset()

    vcc = mcu.vcc.voltage
    p_pwm = mcu.pin(config.pin_pwm)
    pwm_manager = PwmManager(config.pwm, [p_pwm])
#    p_in = mcu.pin(config.pin_x_in)
#    p_out = mcu.pin(config.pin_x_out)
#    p_rail = mcu.pin(config.pin_rail)
    pin_an_in = mcu.pin(config.pin_an_in)
    pin_dig_in = mcu.pin(config.pin_dig_in)

    timer = Stopwatch()

    def meas(reverse):
        def loop(measurements, pwm_value):
                measurements.append(dict(
                                    t=timer.read(),
                                    pwm_value=pwm_value,
                                    Ain=pin_an_in.read_analog(),
                                    Din=pin_dig_in.read_digital_in(),
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
        model=mcu.model,
        pwm_frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )
    return data
