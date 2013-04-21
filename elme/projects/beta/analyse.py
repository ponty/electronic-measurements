from __future__ import division
from numpy.ma.core import size
from softusbduino.util import an2v
from elme.analyse import filter_measurements
from elme.pandasext import ColsProxy, movecol
from uncertainties.unumpy.core import uarray, nominal_values
import numpy as np

def calculate_beta(m, vcc):
        col = ColsProxy(m)
        
        col.Ab=uarray((col.Ab,1))
        col.Ac=uarray((col.Ac,1))
        
        
        col.Ub = an2v(col.Ab, vcc)
        col.Uc = an2v(col.Ac, vcc)

        Rout = 20

        pnp = col.polarity == 'PNP'
        npn = col.polarity == 'NPN'

        col.Urb[pnp] = col.Ub[pnp]
        col.Urb[npn] = vcc - col.Ub[npn]

        col.Urc[pnp] = col.Uc[pnp]
        col.Urc[npn] = vcc - col.Uc[npn]

        col.Ib = col.Urb / (col.Rb + Rout)
        col.Ic = col.Urc / (col.Rc + Rout)
        col.Ie = col.Ib + col.Ic
        col.beta = col.Ic / col.Ib[nominal_values(col.Ib) != 0]

        col.Ue[pnp] = vcc - (Rout * col.Ie[pnp])
        col.Ue[npn] = Rout * col.Ie[npn]

        col.Ube[pnp] = -(col.Ub[pnp] - col.Ue[pnp])
        col.Ube[npn] = (col.Ub[npn] - col.Ue[npn])


def analyse(data):
    config = data.config
    vcc = data.vcc

    m = filter_measurements(
            data.measurements,
            ['B', 'C', 'E', 'polarity'],
            ['Ab', 'Ac'])
    calculate_beta(m, vcc)
    movecol(m, 'beta', 0)
    m = m.sort_index(by='polarity')
    candidates = m[np.logical_and(m.Ube > 0.1, m.Ube < 1)]
    s = candidates.groupby(['polarity', 'B'], sort=False).size()
    ok = s[s==2]
    if len(ok)==1:
        polarity,B=ok.index[0]
        m=m[np.logical_and(m.polarity==polarity,m.B==B)]
    return m
