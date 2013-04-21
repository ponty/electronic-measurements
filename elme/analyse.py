from uncertainties import ufloat, nominal_value
from uncertainties.unumpy.core import uarray
import numpy
import pandas


def ufloatlist(ls, err):
    return [ufloat((x, err)) for x in ls]


# def filtered(ls, name):
#    ls = [x.get(name) for x in ls if name in x]
#    return averaged_median(ufloatlist(ls, 1))


# def groupped_measurements(measurements, keys):
#    d = defaultdict(list)
#    for m in measurements:
#        if len(keys) == 1:
#            tkey = m.get(keys[0])
#        else:
#            tkey = tuple([m.get(k) for k in keys])
#        d[tkey].append(m)
#    return d


def segmented_measurements(measurements, keys, as_index=False):
    return measurements.groupby(keys, sort=False, as_index=as_index)


def averaged_median_arr(e):
    rolling_median_window = 3
#        return e[0]
    try:
        if len(e) >= rolling_median_window:
            e = pandas.rolling_median(
                e, window=rolling_median_window, min_periods=1)
        agg = numpy.mean(e)
    except ValueError:
#        assert 0,e
        agg = None  # e[0]
    return agg


def filter_measurements(measurements, keys, variables=None):
#    grouped = segmented_measurements(measurements[variables+keys], keys)
    grouped = segmented_measurements(measurements, keys)
#    grouped = measurements.groupby(keys, sort=False, as_index=False)
#    for x,y in grouped.items():
#        print 44,x,y
    filtered = grouped.agg(averaged_median_arr)
    return filtered


def calculate_ohm(R, Atop, Amiddle, Abottom, reverse=False):
    Atop = uarray((Atop, 1))
    Amiddle = uarray((Amiddle, 1))
    Abottom = uarray((Abottom, 1))
    a1 = abs(Atop - Amiddle)
    a2 = abs(Amiddle - Abottom)

    if reverse:
#        if nominal_value(a2) < 1:
#            return
        ratio = a1 / a2
    else:
#        if nominal_value(a1) < 1:
#            return
#        print a1, a2
        ratio = a2 / a1
#    print ratio
    Rx = R * ratio
#    Rx -= McuRout
    return Rx
