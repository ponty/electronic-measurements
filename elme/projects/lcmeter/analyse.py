from __future__ import division
from bunch import Bunch
from operator import itemgetter, attrgetter
from softusbduino.filters import averaged_median
from softusbduino.util import an2v
from elme.analyse import groupped_measurements, filtered, calculate_ohm
from uncertainties import ufloat, nominal_value
import math


def maxi(ls, vcc):
    # drop 1%
    ls = [x.Amiddle for x in ls]
    ls.sort()
    drop = int(len(ls) * 0.05)

    a1 = ls[drop + 1]
    a2 = ls[-drop - 1]
#    a = averaged_median()
    A1 = ufloat((a1, 1))
    A2 = ufloat((a2, 1))
    V1 = an2v(A1, vcc)
    V2 = an2v(A2, vcc)
    return (A1, A2), (V1, V2)


def analyse(dw):
    ''


def process(dw):
    data = dw.data
    config = data.config
    vcc = dw.data.vcc

    d = groupped_measurements(data.measurements, ['R', 'frequency'])
    toplist = config.toplist
#    print 66666,toplist
#    print 66666,d
    frequencies = list(set([k[1] for k in d.keys()]))
    frequencies.sort()
    frequencies = filter(lambda e: e is not None, frequencies)
#    print 'frequencies',frequencies

#    for t in toplist:
#        t.Rx=dict()
#        for f in frequencies:
#            ls = d[t.R,f]
# #            print 66666,ls
#            fdic=t['Rx'][f]=dict()
#            if not len(ls):
#                continue
# #            print 66666,ls
#            (Amin,Amax),(V1,V2)= maxi(ls, vcc)
#            fdic['Amin']=Amin
#            fdic['Amax']=Amax
#            fdic['Aavg']=(Amin+Amax)/2
#            fdic['Arange']=Amax-Amin
    results = []
    for t in toplist:
        for f in frequencies:
            resdic = dict()
            ls = d[t.R, f]
#            print 66666,ls
#            fdic = t['Rx'][f] = dict()
#            if not len(ls):
#                continue
#            print 66666,ls
            (Amin, Amax), (V1, V2) = maxi(ls, vcc)
            resdic['frequency'] = f
            resdic['R'] = t.R
            resdic['Amin'] = Amin
            resdic['Amax'] = Amax
            resdic['Aavg'] = (Amin + Amax) / 2

            resdic['Arange'] = Arange = Amax - Amin

            resdic['Rx'] = Rx = calculate_ohm(t.R, 0, Arange,
                                              1023, reverse=True)
            if Rx:
                resdic['Cx'] = 1 / (2 * 3.141 * f * Rx)
                resdic['Lx'] = Rx / (2 * 3.141 * f)

            results += [resdic]
#            t.Atop = filtered(ls, 'Atop')
#            t.Amiddle = filtered(ls, 'Amiddle')
#            t.Abottom = filtered(ls, 'Abottom')

#            t.Rx = calculate_ohm(t.R, t.Atop, t.Amiddle, t.Abottom)

#            if nominal_value(t.Amiddle):
#                t.key = abs(math.log(nominal_value(t.Amiddle)) - math.log(512))
#            else:
#                t.key = 1000
#    toplist.sort(key=itemgetter('key'))
    return results
