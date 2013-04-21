from __future__ import division
from elme.analyse import filter_measurements, calculate_ohm


def analyse(data):
#     config = data.config

    m = filter_measurements(
        data.measurements,
        ['R'],
#        ['Amiddle']
    )
    del m['t']
    m.insert(0, 'Rx', calculate_ohm(m.R, m.Atop, m.Amiddle, m.Abottom))
    return m
