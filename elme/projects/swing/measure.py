from __future__ import division

from bunch import Bunch
import logging
import math
from nanpy.arduinotree import ArduinoTree, ArduinoTree

from elme.projects.swing.analyse import calculate_good_interval
from elme.projects.swing.circuit import Circuit
from elme.pwm import PwmManager
from elme.timer import Stopwatch
from elme.util import fullrange, an2pwm, avr_name


log = logging.getLogger(__name__)

INPUT,OUTPUT=0,1

def measure(config):
    A = config.R2 / config.R1

    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()
    timer = Stopwatch()

    for d in config.loads:
        mcu.pin.get(d.pin_load).reset()

    p_pwm_plus = mcu.pin.get(config.pin_pwm_plus)
    p_pwm_minus = mcu.pin.get(config.pin_pwm_minus)
    pwm_manager = PwmManager(config.pwm, [p_pwm_plus, p_pwm_minus])

    p_in_plus = mcu.pin.get(config.pin_in_plus)
    p_in_minus = mcu.pin.get(config.pin_in_minus)
    p_out = mcu.pin.get(config.pin_out)

#    def noise_filter(fread):
#        filter_size = 5
#        return filters.median_filter(fread, filter_size)

    def meas(R, pwm_values, phase=None):
        def loop(measurements, pwm_index_plus, pwm_index_minus):
                measurements.append(dict(
                                    t=timer.read(),
                                    pwm_index_plus=pwm_index_plus,
                                    pwm_index_minus=pwm_index_minus,
                                    Aplus=p_in_plus.read_analog_value(),
                                    Aminus=p_in_minus.read_analog_value(),
                                    Aout=p_out.read_analog_value(),
                                    Rload=R,
                                    phase=phase,
                                    ))
        measurements = pwm_manager.measure(loop, pwm_values)
        return measurements

    def meas_multi():
        measurements = []

        # unity gain test: Vplus=Vminus
#        ls = [(x, x) for x in fullrange(config.pwm.start, config.pwm.end)]
        measurements += meas(None, pwm_values=None, phase='unity_gain')
#        return measurements
        # determine good range for both input and ouput
#        d2 = data.copy()
#        d2['measurements'] = measurements
        low, high = calculate_good_interval(config, measurements, limit=10)
#        print low, high
        Alow, Ahigh = low + 0.25 * (high - low), low + 0.75 * (high - low)

        low, high = map(an2pwm, [Alow, Ahigh])

        # input_swing test
        # output is always in good range if input is allowed
        avg = (low + high) / 2
        ls = [(
            math.ceil(x + (avg - x) / (A + 1)), x) for x in pwm_manager.range]
        measurements += meas(None, pwm_values=ls, phase='input_range')

        # output_swing test
        # input is always in good range
        loads = [(d.pin_load, d.Rload) for d in config.loads]
        for nr, R in [(None, None)] + loads:
            if nr is not None:
                mcu.pin.get(nr).write_mode(OUTPUT)
                mcu.pin.get(nr).write_digital_value(0)

            # Vminus is fixed in upper range
            Aplus = Circuit(A, Vminus=Ahigh, Vout= -20).Vplus
            ls = [(x, high) for x in fullrange(an2pwm(Aplus), high)]
            measurements += meas(R, pwm_values=ls, phase='output_swing')

            # to increase resolution
            for i in range(9):
                ls = [(x, high - i) for x in fullrange(an2pwm(Aplus), high)]
                measurements += meas(R, pwm_values=ls, phase='output_swing')

            # Vminus is fixed in lower range
            Aplus = Circuit(A, Vminus=Alow, Vout=1040).Vplus
            ls = [(x, low) for x in fullrange(low, an2pwm(Aplus))]

            # to increase resolution
            for i in range(9):
                ls = [(x, low + i) for x in fullrange(low, an2pwm(Aplus))]
                measurements += meas(R, pwm_values=ls, phase='output_swing')

            if nr is not None:
                mcu.pin.get(nr).reset()

        return measurements

    data = Bunch(
        vcc=vcc,
        model=avr_name(mcu),
        pwm_plus_frequency=p_pwm_plus.pwm.frequency,
        pwm_minus_frequency=p_pwm_minus.pwm.frequency,
        measurements=meas_multi(),
    )

    p_pwm_plus.reset()
    p_pwm_minus.reset()
    return data
