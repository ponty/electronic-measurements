from __future__ import division
from matplotlib.ticker import FuncFormatter
from elme.plotutil import FigureWrapper
from elme.projects.esr.analyse import analyse1
import numpy as np


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    fw.addcol(legend='in', y='Ain')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def ohm_plot(data, fig):
    d = analyse1(data)
#    print d
    newdata = dict(measurements=d, project='esr')

#    print 676,newdata
    fw = FigureWrapper(
        newdata, fig, x='frequency', y='R')

    fw.addcol(x='frequency', y='Rx')
    ax = fw.subplot
    ax.set_xscale('log')
    # ax.set_yscale('log')
    return fig


def ohm_invf_plot(data, fig):
    d = analyse1(data)
#    print d
    measurements = d
    newdata = dict(measurements=d, project='esr')

#    print 676,newdata
    fw = FigureWrapper(
        newdata, fig, x='1/frequency', y='Rx')
#    def xtransform(f):
#        return 1000000 / (2 * 3.141 * f)
    fw.addcol(x=lambda e: 1 / (e.frequency), y='Rx')
    ax = fw.subplot
#    fmin = filter(lambda e: e['Rx'] is not None, measurements)[0]['frequency']
    fmin = min(measurements['frequency'])
#    assert 0 ,fmin
    ax.set_autoscale_on(False)
#    @traced

    def Xc(f, c):
        return 1 / (2 * np.pi * f * c / 1e6)
    ax.plot([0, 1 / (fmin)], [0, Xc(fmin, 0.1)], label='100n')
    ax.plot([0, 1 / (fmin)], [0, Xc(fmin, 1)], label='1u')
    ax.plot([0, 1 / (fmin)], [0, Xc(fmin, 10)], label='10u')
    ax.plot([0, 1 / (fmin)], [0, Xc(fmin, 100)], label='100u')
    ax.plot([0, 1 / (fmin)], [0, Xc(fmin, 1000)], label='1000u')

    fw.update_legend()

    def formatter(x, pos):
        if x:
            return int(1.0 / x)
        else:
            return np.inf

    ax.xaxis.set_major_formatter(FuncFormatter(formatter))

    return fig
