from __future__ import division
from elme.timer import Stopwatch
from nanpy.arduinotree import ArduinoTree
from uncertainties import nominal_value

INPUT,OUTPUT=0,1

def measure(config):
    mcu = ArduinoTree()
    mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_enable_input = mcu.pin.get(config.pin_enable_input)

    timer = Stopwatch()

    def measure1(enable_input, repeat):
        if enable_input:
            p_enable_input.write_mode(OUTPUT)
            p_enable_input.write_digital_value(1)
        else:
            p_enable_input.reset()
        measurements = []

        for _ in range(repeat):
            f = mcu.counter.read(config.gate_time)
            measurements.append(dict(
                                t=timer.read(),
                                frequency=nominal_value(f),
                                enable_input=int(enable_input),
                                ))
        return measurements

    measurements = []
#     measurements += measure1(False, config.repeat_disable_input)
#     measurements += measure1(True, config.repeat_enable_input)
    measurements += measure1(False, 8)
    measurements += measure1(True, 8)
    measurements += measure1(False, 8)
    measurements += measure1(True, 15)
    measurements += measure1(False, 8)
    measurements += measure1(True, 30)

    p_enable_input.reset()

    data = dict(
        vcc=vcc,
        model=mcu.avr_name,
        measurements=measurements,
        gate_time=config.gate_time,
    )

    return data
