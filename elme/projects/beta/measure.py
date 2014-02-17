from __future__ import division
from nanpy.arduinotree import ArduinoTree
from elme.timer import Stopwatch
import time


INPUT,OUTPUT=0,1

class VoltageDivider(object):
    '''
    http://en.wikipedia.org/wiki/Voltage_divider
    '''
    def __init__(self, timer, config):
        self.timer = timer
        self.config = config

    def measure(self, R, p_middle, p_bottom, p_bottom_input=None, p_top=None, p_top_input=None, invert=False):
        '''
        p_top
                  X
        p_middle
                  R
        p_bottom_input
        p_bottom
        '''
        timer = self.timer
        config = self.config
        filter_size = config.filter_size

        measurements = []

        if invert:
            top = 0
            bottom = 1
        else:
            top = 1
            bottom = 0
        Abottom = 1023 * bottom
        Atop = 1023 * top

        p_bottom.write_mode(OUTPUT)
        p_bottom.write_digital_value(bottom)
        if p_top:
            p_top.write_mode(OUTPUT)
            p_top.write_digital_value(top)

        # first read is not stable by 1MOhm because of A/D capacitor
        if R > 10000:
            p_middle.read_analog_value()
            p_middle.read_analog_value()
            p_middle.read_analog_value()

        time.sleep(0.02)

        for _ in range(filter_size):
            measurements.append(dict(
                                t=timer.read(),
                                Amiddle=p_middle.read_analog_value(),
                                R=R,
                                ))
        if p_bottom_input:
            for _ in range(filter_size):
                measurements.append(dict(
                                    t=timer.read(),
                                    R=R,
                                    Abottom=p_bottom_input.read_analog_value(),
                                    ))
        else:
            measurements.append(dict(
                                t=timer.read(),
                                R=R,
                                Abottom=Abottom,
                                ))
        if p_top_input:
            for _ in range(filter_size):
                measurements.append(dict(
                                    t=timer.read(),
                                    R=R,
                                    Atop=p_top_input.read_analog_value(),
                                    ))
        else:
            measurements.append(dict(
                                t=timer.read(),
                                R=R,
                                Atop=Atop,
                                ))

        p_bottom.reset()
        if p_top:
            p_top.reset()
        return measurements


def R_elem(ls, i):
    d = dict([(x.R, x) for x in ls])
    k = sorted(d.keys())[i]
    return d[k]


def highR_elem(ls):
    return R_elem(ls, -1)


def lowR_elem(ls):
    return R_elem(ls, 0)


def measure(config):
    mcu = ArduinoTree()
    mcu.soft_reset()
    vcc = mcu.vcc.read()

    timer = Stopwatch()

    def measure_beta(nodeB, nodeC, nodeE, polarity):
        measurements = []
        pB = mcu.pin.get(nodeB.pin_middle)
        pC = mcu.pin.get(nodeC.pin_middle)
        pE = mcu.pin.get(nodeE.pin_middle)

        elemRb = highR_elem(nodeB.toplist)
        elemRc = lowR_elem(nodeC.toplist)

        pRb = mcu.pin.get(elemRb.pin_rail)
        pRc = mcu.pin.get(elemRc.pin_rail)

        Rb = elemRb.R
        Rc = elemRc.R

        def read(pin):
            return pin.analog_in().u_value

        def delay():
            time.sleep(1 / 1000.0)

        pB.write_mode(INPUT)
        pC.write_mode(INPUT)
        pE.write_mode(OUTPUT)
        pRb.write_mode(OUTPUT)
        pRc.write_mode(OUTPUT)

        if (polarity == 'NPN'):
            pE.write_digital_value(0)
            pRb.write_digital_value(1)
            pRc.write_digital_value(1)
        else:
            pE.write_digital_value(1)
            pRb.write_digital_value(0)
            pRc.write_digital_value(0)

        delay()

        pB.read_analog_value()
        pB.read_analog_value()
        pB.read_analog_value()

        for _ in range(config.filter_size):
            measurements.append(dict(
                                t=timer.read(),
                                Ab=pB.read_analog_value(),
                                Rb=Rb,
                                Rc=Rc,
                                polarity=polarity,
                                B=nodeB.name,
                                C=nodeC.name,
                                E=nodeE.name,
                                ))

        pC.read_analog_value()
        pC.read_analog_value()
        pC.read_analog_value()

        for _ in range(config.filter_size):
            measurements.append(dict(
                                t=timer.read(),
                                Ac=pC.read_analog_value(),
                                Rb=Rb,
                                Rc=Rc,
                                polarity=polarity,
                                B=nodeB.name,
                                C=nodeC.name,
                                E=nodeE.name,
                                ))

        pB.reset()
        pC.reset()
        pE.reset()
        pRb.reset()
        pRc.reset()
        return measurements

    measurements = []
    combinations = [(0, 1, 2), (0, 2, 1),
                    (1, 2, 0), (1, 0, 2),
                    (2, 1, 0), (2, 0, 1),
                    ]
    for k1, k2, k3 in combinations:
        nodeB = config.nodes[k1]
        nodeC = config.nodes[k2]
        nodeE = config.nodes[k3]
        measurements += measure_beta(nodeB, nodeC, nodeE, polarity='PNP')
        measurements += measure_beta(nodeB, nodeC, nodeE, polarity='NPN')

    data = dict(
        vcc=vcc,
        model=mcu.avr_name,
        measurements=measurements,
    )

    return data
