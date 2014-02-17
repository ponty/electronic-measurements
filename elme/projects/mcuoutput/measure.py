from __future__ import division
from nanpy.arduinotree import ArduinoTree
from elme.pwm import PwmManager
from elme.timer import Stopwatch
import logging
from nanpy.arduinotree import ArduinoTree

log = logging.getLogger(__name__)


INPUT,OUTPUT=0,1

def measure(config):
    mcu = ArduinoTree()
    mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_pwm = mcu.pin.get(config.pin_pwm)
    pwm_manager = PwmManager(config.pwm, [p_pwm])
#    pwm = p_pwm.pwm
    p_amp = mcu.pin.get(config.pin_amp_out)
    p_out_an = mcu.pin.get(config.pin_out_an)
    p_out_dig = mcu.pin.get(config.pin_out_dig)
    timer = Stopwatch()

#    pwm.divisor = config.pwm.divisor

    def meas(dig_out):
        p_out_dig.write_digital_value(dig_out)

        def loop(measurements, pwm_value):
            measurements.append(dict(
                                t=timer.read(),
                                pwm_value=pwm_value,
                                Aamp=p_amp.read_analog_value(),
                                Aout=p_out_an.read_analog_value(),
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
        model=mcu.avr_name,
        frequency=p_pwm.pwm.frequency,
        measurements=measurements,
    )

    return data
