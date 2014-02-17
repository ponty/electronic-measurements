from __future__ import division
from bunch import bunchify
from elme.analyse import filter_measurements
from elme.projects.swing.circuit import Circuit

# @traced


def longest_good_interval(ycol, limit):
    good = [abs(y) < limit for y in ycol]

    intervals = []
    inside = False
    for i, b in enumerate([False] + good + [False]):
        i -= 1
        if not inside:
            r = [None, None]
            if b:
                inside = True
                r[0] = i
        if inside:
            if not b:
                inside = False
                r[1] = i - 1
                intervals.append(r)
#    print intervals
    intervals.sort(key=lambda r: r[1] - r[0], reverse=True)
    if len(intervals):
        return intervals[0]


def calculate_good_interval(config, measurements, limit):
#    dw = DataWrapper(data)
    A = config.R2 / config.R1
    measurements = bunchify(measurements)
    for x in measurements:
        if x.phase == 'unity_gain':
            x.Aout_expected = Circuit(A, Vminus=x.Aminus, Vplus=x.Aplus).Vout
            x.dA = (x.Aout - x.Aout_expected)
    R = None

    def filter_func(x):
        return x.Rload == R and x.phase == 'unity_gain'
    xcol = [e.Aout_expected for e in measurements if filter_func(e)]
    ycol = [e.dA for e in measurements if filter_func(e)]
#    xcol, ycol = dw.cols4plot(xname='',
#                              yname='dV',
#                              filter_func=filter_func,
#                              median_filters=[9, 9, 9],
#                              )
#    ls = zip(xcol, ycol)
    interv = longest_good_interval(ycol, limit)
    if interv:
        return xcol[interv[0]], xcol[interv[1]]

# def good_range(measurements,A):
#        low, high = 0, 255
#        for x in measurements:
#            Vplus = x['Vplus']
#            Vminus = x['Vminus']
#            Vout = x['Vout']
#            pwm_index_plus = x['pwm_index_plus']
#            Vx = Circuit(A, Vminus=Vminus, Vplus=Vplus).Vout
#    #        if not x['unity_gain']:
#    #            continue
# #            print abs(Vx - Vout), Vx, Vout
#            ok = abs(Vx - Vout) < 0.200
#            if Vplus <= 2.5:
#                if not ok and pwm_index_plus > low:
#                    low = pwm_index_plus
#            else:
#                if not ok and pwm_index_plus < high:
#                    high = pwm_index_plus
#        return dict(pwm=(low, high))

NO_LOAD = 1e9


def extend(data):
#    data.measurements.to_csv('y.csv')

    config = data.config
    vcc = data.vcc

#    m=data.measurements
##    data.measurements['Rload']=data.measurements['Rload'].fillna(NO_LOAD),
#    m['Rload']=m['Rload'].astype(str).fillna(NO_LOAD)
#    data.measurements=m

    m = filter_measurements(
        data.measurements.fillna(NO_LOAD),
#        ['Rload','phase'],
        ['phase', 'Rload', 'pwm_index_plus', 'pwm_index_minus'],
        ['Aminus', 'Aplus', 'Aout']
    )
#    m.to_csv('x.csv')
#    print set(data.measurements['phase'])
#    print m.to_string()
#    print set(m['phase'])
#    assert 0
    A = config.R2 / config.R1

    m['Vminus'] = an2v(m.Aminus, vcc)
    m['Vplus'] = an2v(m.Aplus, vcc)
    m['Vout'] = an2v(m.Aout, vcc)
    m['Vout_expected'] = Circuit(A, Vminus=m.Vminus, Vplus=m.Vplus).Vout
    m['Vout_diff'] = (m.Vout - m.Vout_expected)
    m['Vopamp_minus'] = Circuit(A, Vminus=m.Vminus, Vout=m.Vout).Vplus
    m['Vin_diff'] = (m.Vopamp_minus - m.Vplus)
    data.measurements = m
#    m.to_csv('x.csv')
#    for x in data.measurements:
#        x.Vminus = an2v(x.Aminus, vcc)
#        x.Vplus = an2v(x.Aplus, vcc)
#        x.Vout = an2v(x.Aout, vcc)
#        x.Vout_expected = Circuit(A, Vminus=x.Vminus, Vplus=x.Vplus).Vout
#        x.Vout_diff = (x.Vout - x.Vout_expected)
#        x.Vopamp_minus = Circuit(A, Vminus=x.Vminus, Vout=x.Vout).Vplus
#        x.Vin_diff = (x.Vopamp_minus - x.Vplus)
