from __future__ import division

from nanpy.arduinotree import ArduinoTree
import time

from elme.timer import Stopwatch, TimeOutError
from elme.util import avr_name


INPUT,OUTPUT=0,1

def timeout_loop(timeout, loop_func):
    timer2 = Stopwatch()
    while 1:
        if not loop_func():
                break
        timer2.check_timeout(timeout)


def measure(config):
    mcu = ArduinoTree()
#     mcu.soft_reset()
    vcc = mcu.vcc.read()
    p_middle = mcu.pin.get(config.pin_middle)
    measurements = []

    timer = Stopwatch()
    timeout = config.charge_timeout

    toplist = sorted(config.toplist, key=lambda e: e.R)
    top_charge = toplist[0]
    pin_charge = mcu.pin.get(top_charge.pin_rail)

    def         setcharge(value, limit):
        measurements = []
        pin_charge.write_mode(OUTPUT)
        pin_charge.write_digital_value(value)

        def loop_func():
            a = p_middle.read_analog_value()
            measurements.append(dict(
                                t=timer.read(),
                                Amiddle=a,
                                R=top_charge.R,
                                charge=1,
                                #                                 cont=1,
                                ))
            if value == 1:
                if a > limit:
                    return False
            else:
                if a < limit:
                    return False
            return True
        timeout_loop(timeout, loop_func)

        pin_charge.reset()
        return measurements

    def         discharge(limit=None):
        if limit is None:
            limit = config.lower_limit
        return setcharge(value=0, limit=limit)

    def         charge(limit=None):
        if limit is None:
            limit = config.upper_limit
        return setcharge(value=1, limit=limit)

    def measure1(measurements, pin_rail, pin_input, R):
        def loop_func():
            Amiddle = p_middle.read_analog_value()
            measurements.append(dict(
                                t=timer.read(),
                                Amiddle=Amiddle,
                                R=R,
                                charge=0,
                                # cont=int(tmeasure is None),
                                ))
            if Amiddle < config.lower_limit:
                    return False
            return True

        measurements += charge()

        pin_rail.write_mode(OUTPUT)
        pin_rail.write_digital_value(0)

        # first read is not stable by 1MOhm because of A/D capacitor
        p_middle.read_analog_value()
#        if tmeasure:
#            loop_func()
#            time.sleep(tmeasure)
#            loop_func()
#        else:
        timeout_loop(timeout, loop_func)

#        pin_rail.reset()

    for d in toplist:
        pin_rail = mcu.pin.get(d['pin_rail'])
        pin_input = mcu.pin.get(d['pin_input'])
        R = d['R']
#        timer3 = Stopwatch()
        try:
            measure1(measurements, pin_rail, pin_input, R)
        except TimeOutError as e:
            print e
            break
        finally:
#        tm=timer3.read()
#        tm*=0.9
#        print tm
#        measure1(measurements, pin_rail, pin_input, R, tm)

            pin_rail.reset()

    data = dict(
        vcc=vcc,
        model=avr_name(mcu),
        measurements=measurements,
    )

    return data
