from __future__ import division
from elme.pwm import PwmManager
from elme.timer import Stopwatch
from nanpy.arduinotree import ArduinoTree
import logging

log = logging.getLogger(__name__)


def measure(config):
    mcu = ArduinoTree()
    mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_pwm = mcu.pin.get(config.pin_pwm)
    pwm_manager = PwmManager(config.pwm, [p_pwm])
    p_amp = mcu.pin.get(config.pin_amp_out)
    p_in = mcu.pin.get(config.pin_x_in)
    p_out = mcu.pin.get(config.pin_x_out)
    timer = Stopwatch()

    def meas(reverse):
        def loop(measurements, pwm_value):
                measurements.append(dict(
                                    t=timer.read(),
                                    pwm_value=pwm_value,
                                    Aamp=p_amp.read_analog_value(),
                                    Ain=p_in.read_analog_value(),
                                    Aout=p_out.read_analog_value(),
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
        model=mcu.avr_name,
        pwm_frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )
    return data
