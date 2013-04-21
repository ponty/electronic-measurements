from __future__ import division
from softusbduino.util import an2v
from elme.analyse import filter_measurements
from elme.pandasext import ColsProxy


def extend(data):
    m = filter_measurements(
        data.measurements,
        ['reverse', 'pwm_value'],
        ['Aout', 'Ain', 'Aamp'])

    R = data.config.R
    vcc = data.vcc

    data.Vmax = data.vcc
    data.Imax = data.vcc / R

    col = ColsProxy(m)
    col.Vin = an2v(col.Ain, vcc)
    col.Vout = an2v(col.Aout, vcc)
    col.Vamp = an2v(col.Aamp, vcc)
    #m = m.sort_index(by='Vin')

    data.measurements = m
