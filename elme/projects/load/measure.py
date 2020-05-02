from __future__ import division

import logging
from nanpy.arduinotree import ArduinoTree
from time import sleep
import time

from elme.timer import Stopwatch
from elme.util import avr_name


# from elme.pwm import PwmManager
INPUT, OUTPUT = 0, 1

log = logging.getLogger(__name__)

resistors = [
    ('D2', 1),
    ('D3', 1),
    ('D4', 1),
    ('D5', 2),
    ('D6', 4.1),
    ('D7', 8.2),
    ('D8', 16.5),
    ('D9', 33),
    ('D10', 68),
]
bits = [
    [0, 1],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8],
]


def to_binary_list(i, length):
    ls = [int(x) for x in bin(i)[2:]]
    ls = (length - len(ls)) * [0] + ls
    return ls


class Hardware(object):

    def __init__(self, config):
        self.mcu = ArduinoTree()
        self.vcc = self.mcu.vcc.read()
        self.p_volt_in = self.mcu.pin.get(config.pin_volt_in)
        self.p_current_in = self.mcu.pin.get(config.pin_current_in)

        self.pins = [self.mcu.pin.get(k) for k, v in resistors]
        self.res = [v for k, v in resistors]
        for p in self.pins:
            p.write_mode(OUTPUT)

        self.set_off()

    def set_off(self):
        # turn off all swicthes
        for p in self.pins:
            p.write_digital_value(0)

    def set_r_mask(self, r_mask):
        for ip, b in enumerate(to_binary_list(r_mask, len(bits))):
            lsbits = bits[ip]
            for bit in lsbits:
                p = self.pins[bit]
                p.write_digital_value(b)
#             print '---', pins[ip], b

    def get_r_mask_ohm(self, r_mask):
        r_all = 0
        for ip, b in enumerate(to_binary_list(r_mask, len(bits))):
            lsbits = bits[ip]
            for bit in lsbits:
                r = self.res[bit]
                if b:
                    r_all += 1 / r
        if r_all == 0:
            return -1
        r_all = 1 / r_all
#         print '---', r_all
        return r_all

    def read_Ain(self):
        return self.p_volt_in.read_analog_value()

    def read_Ahall(self):
        return self.p_current_in.read_analog_value()

    def read_Vcc(self):
        return self.mcu.vcc.read()

def measure(config):
    timer = Stopwatch()
    hw = Hardware(config)
    max_r_mask = 2 ** (len(bits)) - 1
    sleep_time = config.sleep_time
    measurements = []
    for r_mask in range(max_r_mask + 1):
        hw.set_r_mask(r_mask)
        sleep(sleep_time)
        measurements.append(dict(
                            t=timer.read(),
                            Ain=hw.read_Ain(),
                            Ahall=hw.read_Ahall(),
                            r_mask=r_mask,
                            ))
    
    hw.set_off()
    
    data = dict(
        vcc=hw.vcc,
        model=avr_name(hw.mcu),
        measurements=measurements,
    )

    return data
