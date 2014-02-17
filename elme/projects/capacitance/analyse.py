from __future__ import division
from elme.analyse import segmented_measurements
from elme.pandasext import ColsProxy, movecol
from pandas.core.frame import DataFrame
from uncertainties import ufloat, nominal_value, umath, unumpy
from uncertainties.unumpy.core import uarray
import numpy as np
from elme.util import an2v


terror = 1e-3  # estimation

Rout = 25


def regc(df, R):
    R += Rout
    xi = df['t'].values
    dt = xi[-1] - xi[0]
    A = np.array([xi, np.ones(len(xi))])
    y = df['Amiddle'].values
    y = np.log(y)
    w = np.linalg.lstsq(A.T, y)[0]
    return -1 / w[0] / R


def replace0(ls):
    return [np.nan if x == 0 else x for x in ls]


def calculate_c(A1, A2, R, t1, t2):
    t = t2 - t1
    t = uarray((t, terror))
    A1 = uarray((replace0(A1), 1))
    A2 = uarray((replace0(A2), 1))
    # http://en.wikipedia.org/wiki/RC_circuit
#    if A1 > 0 and A2 > 0 and R > 0 and A1 != A2:
    c = -t / (R * unumpy.log(A2 / A1))

    return c


def analyse(data):
    config = data.config
    vcc = data.vcc
    m = data.measurements
    grouped = segmented_measurements(m, ['charge', 'R'], as_index=1)

    def voltage(measurement):
        return u_an2v(measurement.Amiddle, vcc)

    def first(ls):
        return ls.values[0]

    def last(ls):
        return ls.values[-1]
    t = grouped['t'].agg(dict(t1=first, t2=last))
    A = grouped['Amiddle'].agg(dict(A1=first, A2=last))
    mreg = DataFrame([(charge, R, regc(g, R)) for (charge, R), g in grouped],
                     columns=['charge', 'R', 'Creg'])

    df = A.join(t)
    df = df.reset_index()

    df = df[df['charge'] == 0]
    del df['charge']

    col = ColsProxy(df)

    col.Creg = mreg['Creg']
    col.dt = col.t2 - col.t1
    col.C = calculate_c(col.A1, col.A2, col.R, col.t1, col.t2)

    movecol(df, 'Creg', 0)
    movecol(df, 'C', 0)

    return df
