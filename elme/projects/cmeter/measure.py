from __future__ import division
from elme.timer import Stopwatch
from softusbduino import Arduino
from softusbduino.const import OUTPUT
from softusbduino.const import INPUT
from uncertainties import nominal_value


def measure(config):
    mcu = Arduino()
    mcu.pins.reset()
    vcc = mcu.vcc.voltage
    p_enable_input = mcu.pin(config.pin_enable_input)

    timer = Stopwatch()

    def measure1(enable_input, repeat):
        if enable_input:
            p_enable_input.write_mode(OUTPUT)
            p_enable_input.write_digital_out(1)
        else:
            p_enable_input.reset()
        measurements = []

        for _ in range(repeat):
            f = mcu.counter.run(config.gate_time)
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
        model=mcu.model,
        measurements=measurements,
        gate_time=mcu.counter.gate_time,
    )

    return data
