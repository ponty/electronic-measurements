from __future__ import division
from elme.analyse import filter_measurements, calculate_ohm
from elme.formating import format_ohmE12
from uncertainties.unumpy.core import nominal_values


def analyse(data):
    m = filter_measurements(
        data.measurements,
        ['R'],
    )
    del m['t']
    m.insert(0, 'Rx', calculate_ohm(m.R, m.Atop, m.Amiddle, m.Abottom))
    m.insert(0, 'Rx_E12', map(format_ohmE12, nominal_values(m.Rx)))
    return m
