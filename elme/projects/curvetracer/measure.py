from __future__ import division
from softusbduino import Arduino
from softusbduino.const import OUTPUT
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
    p_amp = mcu.pin(config.pin_amp_out)
    p_in = mcu.pin(config.pin_x_in)
    p_out = mcu.pin(config.pin_x_out)
    p_rail = mcu.pin(config.pin_rail)
    timer = Stopwatch()

    def meas(rail):
        p_rail.write_mode(OUTPUT)
        p_rail.write_digital_out(rail)

        def loop(measurements, pwm_value):
                measurements.append(dict(
                                    t=timer.read(),
                                    pwm_value=pwm_value,
                                    Aamp=p_amp.read_analog(),
                                    Ain=p_in.read_analog(),
                                    Aout=p_out.read_analog(),
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
        model=mcu.model,
        pwm_frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )
    return data
