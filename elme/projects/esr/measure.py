from __future__ import division
from math import log10
from numpy import logspace
from softusbduino.arduino import Arduino
from softusbduino.const import OUTPUT
from elme.timer import Stopwatch
from elme.util import sleep_and_read
import time


def measure(config):
    mcu = Arduino()
    mcu.pins.reset()

    vcc = mcu.vcc.voltage
    p_in = mcu.pin(config.pin_in)
    p_pwm = mcu.pin(config.pin_pwm)
#    p_pwm2 = mcu.pin('D8')
#    p_pwm_check = mcu.pin(config.pin_pwm_check)
    timer = Stopwatch()

    p_pwm.write_mode(OUTPUT)
#    p_pwm2.write_mode(OUTPUT)

#    def meas_max():
#        time.sleep(1)
#        p_pwm2.write_digital_out(1)
#
#        time.sleep(config.settle_time)
#
#        measurements = []
#        for i in range(config.window):
#            timer.measure()
#            Apwm = p_pwm_check.read_analog()
#            measurements.append(dict(
#                                t=timer.relativ(),
# #                                pwm_value=pwm_value,
#                                Apwm=Apwm,
#                                ))
#        return measurements

    pwm = p_pwm.pwm
#    pwm.divisor = 1

    def meas(frequency, dc=0):
        if frequency == 0:
            pwm.write_value(dc * 255)
        else:
            pwm.set_high_freq_around(frequency)
            frequency = pwm.read_frequency()
#        pwm_value = int(pwm_value)
#        pwm.write_value(pwm_value)

        # there is a slow drift when starting the measurement
        # so it is better to read continuously while sleeping
        sleep_and_read(config.settle_time, p_in)
        # time.sleep(config.settle_time)

        measurements = []
        for i in range(config.window):
            Ain = p_in.read_analog()
            measurements.append(dict(
                                t=timer.read(),
                                Ain=Ain,
                                frequency=frequency,
                                dc=dc,
                                ))
        return measurements

    measurements = []

    measurements += meas(0, 0)
    measurements += meas(0, 1)
    for f in logspace(log10(config.freq.min), log10(config.freq.max), config.freq.steps):
        measurements += meas(f)

    data = dict(
        vcc=vcc,
        model=mcu.model,
        measurements=measurements,
    )

    p_in.reset()
    p_pwm.reset()

    return data
