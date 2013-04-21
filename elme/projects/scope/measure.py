from softusbduino.arduino import Arduino
from elme.timer import Stopwatch
import logging

log = logging.getLogger(__name__)


def measure(config, stop_condition=None):
    mcu = Arduino()
    if config.reset:
        mcu.pins.reset()
    vcc = mcu.vcc.voltage
    pin = mcu.pin(config.pin)
    interval = config.interval

    measurements = []
    timer = Stopwatch()
    while 1:
        measurements.append(dict(
                            t=timer.read(),
                            A=pin.read_analog(),
                            ))
        if timer.last > interval:
            break
        if stop_condition:
            if stop_condition(timer):
                break

    data = dict(
        vcc=vcc,
        model=mcu.model,
        measurements=measurements,
    )

    return data
