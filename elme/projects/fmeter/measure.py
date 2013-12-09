from __future__ import division
from elme.timer import Stopwatch
from softusbduino import Arduino
from uncertainties import nominal_value


def measure(config):
    mcu = Arduino()
#     mcu.pins.reset()
    vcc = mcu.vcc.voltage

    timer = Stopwatch()

    measurements = []

#     for _ in range(config.repeat):
    while 1:
        f = mcu.counter.run(config.gate_time)
        measurements.append(dict(
                            t=timer.read(),
                            frequency=nominal_value(f),
                            ))
        if timer.last > config.interval:
            break

    data = dict(
        vcc=vcc,
        model=mcu.model,
        measurements=measurements,
        gate_time=mcu.counter.gate_time,
    )

    return data
