from __future__ import division
from elme.timer import Stopwatch
from nanpy.arduinotree import ArduinoTree
from uncertainties import nominal_value


def measure(config):
    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()

    timer = Stopwatch()

    measurements = []

#     for _ in range(config.repeat):
    while 1:
        f = mcu.counter.read(config.gate_time)
        measurements.append(dict(
                            t=timer.read(),
                            frequency=nominal_value(f),
                            ))
        if timer.last > config.interval:
            break

    data = dict(
        vcc=vcc,
        model=mcu.avr_name,
        measurements=measurements,
        gate_time=config.gate_time,
    )

    return data
