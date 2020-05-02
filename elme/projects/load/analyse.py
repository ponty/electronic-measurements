from __future__ import division
from elme.analyse import filter_measurements
from elme.pandasext import ColsProxy
import pandas
from elme.util import an2v

def analyse(data):
    pass


def calc_Vin(Ain, vcc, volt_division):
    Vin = an2v(Ain, vcc) * volt_division
    return Vin

def calc_Iin(Ahall, vcc, hall_VperA):
    Iin = an2v(512 - Ahall, vcc) / hall_VperA
    return Iin

def extend(data):
    m = data.measurements
#     print 'm',m
#     m = filter_measurements(
#         data.measurements,
#         ['pwm_value', 'rail'],
#         ['Aout', 'Ain', 'Aamp'])

#     R = data.config.R
    volt_division = data.config.volt_division
    hall_VperA = data.config.hall_VperA
    vcc = data.vcc

#     data.Vmax = data.vcc
#     data.Imax = data.vcc / R


    col = ColsProxy(m)
    col.Vin = calc_Vin(col.Ain, vcc, volt_division)
#     col.Vout = an2v(col.Aout, vcc)
#     col.Vamp = an2v(col.Aamp, vcc)
#     col.Vx = col.Vout - col.Vin
    col.Iin = an2v(512 - col.Ahall, vcc) / hall_VperA
#     m = m.sort_index(by='Vx')

#     col.I = pandas.rolling_median(col.I, window=5)

#     print 'col',col
#     print 'm',m
    data.measurements = m
