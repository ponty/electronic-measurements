from __future__ import division
from decotrace import traced
from elme.analyse import filter_measurements, calculate_ohm

pi = 3.141


def calc_c(f, f0, C0):
                return ((f0 / f) ** 2 - 1) * C0
def calc_l(f, f0, C0):
                return 1 / (C0 * 4 * pi ** 2) * (1 / (f ** 2) - 1 / (f0 ** 2))


def analyse(data):
    df = data.measurements

    f0 = df[df.enable_input == 0].frequency.iloc[-1]
    f = df[df.enable_input > 0].frequency.iloc[-1]
    C0 = float(data.config[ 'C0'])
    Cx = calc_c(f, f0, C0)
    Lx = calc_l(f, f0, C0)
    return dict(
                C0=C0,
                Cx=Cx,
                Lx=Lx,
                f0=f0,
                f=f,
                )
