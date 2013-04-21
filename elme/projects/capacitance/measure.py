from __future__ import division
from softusbduino import Arduino
from softusbduino.const import OUTPUT, INPUT
from elme.timer import Stopwatch, TimeOutError
import time


def timeout_loop(timeout, loop_func):
    timer2 = Stopwatch()
    while 1:
        if not loop_func():
                break
        timer2.check_timeout(timeout)


def measure(config):
    mcu = Arduino()
    mcu.pins.reset()
    vcc = mcu.vcc.voltage
    p_middle = mcu.pin(config.pin_middle)
    measurements = []

    timer = Stopwatch()
    timeout = config.charge_timeout

    toplist = sorted(config.toplist, key=lambda e: e.R)
    top_charge = toplist[0]
    pin_charge = mcu.pin(top_charge.pin_rail)

    def         setcharge(value, limit):
        measurements = []
        pin_charge.write_mode(OUTPUT)
        pin_charge.write_digital_out(value)

        def loop_func():
            a = p_middle.read_analog()
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
            Amiddle = p_middle.read_analog()
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
        pin_rail.write_digital_out(0)

        # first read is not stable by 1MOhm because of A/D capacitor
        p_middle.read_analog()
#        if tmeasure:
#            loop_func()
#            time.sleep(tmeasure)
#            loop_func()
#        else:
        timeout_loop(timeout, loop_func)

#        pin_rail.reset()

    for d in toplist:
        pin_rail = mcu.pin(d['pin_rail'])
        pin_input = mcu.pin(d['pin_input'])
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
        model=mcu.model,
        measurements=measurements,
    )

    return data
