from softusbduino.const import OUTPUT
from elme.util import fullrange
import time


class PwmManager(object):
    def __init__(self, config, pins):
        self.config = config
        self.pins = pins
        for p in pins:
            p.write_mode(OUTPUT)
            p.pwm.write_divisor(config.divisor)
        self.range = fullrange(self.config.start, self.config.end)

    def measure(self, loop, pwm_values=None, reverse=False):
        if not pwm_values:
            pwm_values = []
            for i in self.range:
                pwm_values += [[i] * len(self.pins)]
        measurements = []

        if reverse:
            pwm_values = reversed(pwm_values)

        last_pwm_indeces = None
        first = True
        for lsi in pwm_values:
            assert len(lsi) == len(self.pins)

            # move first to next value then back for faster speed
            #  17 -> 19 -> 18
            if last_pwm_indeces:
                for i, ilast, p in zip(lsi, last_pwm_indeces, self.pins):
                    assert abs(i - ilast) <= 1  # max step is 1!
                    inext = i + i - ilast
                    if inext >= 0 and inext <= 255:
                        p.pwm.write_value(inext)

            for i, p in zip(lsi, self.pins):
                p.pwm.write_value(i)

            if first:
                time.sleep(self.config.wait_before_big_step)
                first = False
            else:
                time.sleep(self.config.wait_before_step)

            for _ in range(self.config.repeat):
                loop(measurements, *lsi)

            last_pwm_indeces = lsi
        return measurements
