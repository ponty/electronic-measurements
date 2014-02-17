from __future__ import division
from elme.util import an2v


def analyse(data):
    m = data.measurements

    vcc = data.vcc

    stats = m.Ain.describe()

    count = stats['count']
    Amean = stats['mean']
    Amin = stats['min']
    Amax = stats['max']
    Arange = Amax - Amin
    Amiddle = (Amin + Amax) / 2
    duty_cycle = len(m.Ain[m.Ain > Amiddle]) / len(m.Ain)

    Astd = stats['std']
    Arms = (Astd ** 2 + Amean ** 2) ** 0.5

    return dict(
                count=count,
        Amin=Amin,
        Amax=Amax,
        Arange=Arange,
        Amean=Amean,
        duty_cycle=duty_cycle,
        Astd=Astd,
        Arms=Arms,
        Vmean=an2v(Amean, vcc),
        Vstd=an2v(Astd, vcc),
        Vrms=an2v(Arms, vcc),
        Vmin=an2v(Amin, vcc),
        Vmax=an2v(Amax, vcc),
        Vrange=an2v(Arange, vcc),
    )
