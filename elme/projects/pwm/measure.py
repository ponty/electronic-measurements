from __future__ import division
from nanpy.arduinotree import ArduinoTree
from elme.pwm import PwmManager
from elme.timer import Stopwatch
import logging

log = logging.getLogger(__name__)


def measure(config):
    mcu = ArduinoTree()
    mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_pwm = mcu.pin.get(config.pin_pwm)
    pwm_manager = PwmManager(config.pwm, [p_pwm])
    p_in = mcu.pin.get(config.pin_in)
    timer = Stopwatch()

    # max freq
#    pwm.divisor = config.pwm.divisor
#    print 'freq=%s' % pwm.frequency

    def meas():
        def loop(measurements, pwm_value):
            measurements.append(dict(
                                t=timer.read(),
                                pwm_value=pwm_value,
                                Ain=p_in.read_analog_value(),
                                ))
        measurements = pwm_manager.measure(loop)

        return measurements

#        pwm.write_value(config.pwm.start)

#        time.sleep(1)

#        measurements = []
#        tstart = time.time()
#        for i in range(config.pwm.start, config.pwm.end + 1):
#            pwm.write_value(i)
#            time.sleep(config.wait)

#            A = p_in.read_analog_value()
#            measurements.append(dict(
#                                t=timer.read(),
#                                pwm_value=i,
#                                A=A,
#                                ))
#        return measurements

    data = dict(
        vcc=vcc,
        model=mcu.avr_name,
        measurements=meas(),
        frequency=p_pwm.pwm.frequency,
    )

    p_pwm.reset()

    return data
