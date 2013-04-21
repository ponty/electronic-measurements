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
#    pwm = p_pwm.pwm
    p_amp = mcu.pin(config.pin_amp_out)
    p_out_an = mcu.pin(config.pin_out_an)
    p_out_dig = mcu.pin(config.pin_out_dig)
    timer = Stopwatch()

#    pwm.divisor = config.pwm.divisor

    def meas(dig_out):
        p_out_dig.write_digital_out(dig_out)

        def loop(measurements, pwm_value):
            measurements.append(dict(
                                t=timer.read(),
                                pwm_value=pwm_value,
                                Aamp=p_amp.read_analog(),
                                Aout=p_out_an.read_analog(),
                                Dout=dig_out,
                                ))
        measurements = pwm_manager.measure(loop)

        return measurements

    measurements = []

    p_out_dig.write_mode(OUTPUT)
    measurements += meas(1)
    measurements += meas(0)

    p_out_dig.reset()
    p_pwm.reset()

    data = dict(
        vcc=vcc,
        model=mcu.model,
        frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )

    return data
