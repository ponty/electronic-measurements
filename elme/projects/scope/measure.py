from elme.timer import Stopwatch
import logging
from nanpy.arduinotree import ArduinoTree

log = logging.getLogger(__name__)


def measure(config, stop_condition=None):
    mcu = ArduinoTree()
    if config.reset:
        mcu.soft_reset()
    vcc = mcu.vcc.read()
    pin = mcu.pin.get(config.pin)
    interval = config.interval

    measurements = []
    timer = Stopwatch()
    while 1:
        measurements.append(dict(
                            t=timer.read(),
                            A=pin.read_analog_value(),
                            ))
        if timer.last > interval:
            break
        if stop_condition:
            if stop_condition(timer):
                break

    data = dict(
        vcc=vcc,
        model=mcu.avr_name,
        measurements=measurements,
    )

    return data
