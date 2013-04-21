from __future__ import division
from softusbduino.util import an2v
from elme.analyse import filter_measurements
from elme.pandasext import ColsProxy
import pandas


def extend(data):
    m = filter_measurements(
        data.measurements,
        ['pwm_value', 'rail'],
        ['Aout', 'Ain', 'Aamp'])

    R = data.config.R
    vcc = data.vcc

    data.Vmax = data.vcc
    data.Imax = data.vcc / R

    col = ColsProxy(m)
    col.Vin = an2v(col.Ain, vcc)
    col.Vout = an2v(col.Aout, vcc)
    col.Vamp = an2v(col.Aamp, vcc)
    col.Vx = col.Vout - col.Vin
    col.I = (col.Vin - col.Vamp) / R
    m = m.sort_index(by='Vx')

    col.I = pandas.rolling_median(col.I, window=5)

    data.measurements = m
