from __future__ import division
from copy import copy
from elme.plotutil import FigureWrapper
from elme.projects.acvoltmeter.analyse import analyse
import numpy as np


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(data, fig, x='time', y='analog_value',
                       convert2voltage=voltage)

    fw.addcol(legend='in', y='Ain')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def histo_plot(data, fig):
    ycol = data['measurements']['Ain']

    ax = fig.add_subplot(111)
    nbins = 20
    n, bins, patches = ax.hist(ycol, nbins, normed=0, histtype='stepfilled')
    d = analyse(data)
    avg = d['count'] / nbins

    # sawtooth
    ax.plot([d['Amin'], d['Amax']], [avg, avg], label='sawtooth')

    # sine
    xarr = np.linspace(d['Amin'], d['Amax'], num=50)

    def sine_bins(x):
        xb = copy(x)
        xb -= (d['Amax'] + d['Amin']) / 2
        xb /= d['Arange'] / 2
        y = 1 / (1 - xb ** 2) ** 0.5
        y *= avg / (np.pi / 2)
        return y
#     print(xarr, sine_bins(xarr))
    ax.plot(xarr, sine_bins(xarr), label='sine')

    ax.set_ylim(bottom=0)
    ax.set_xlim(0, 1023)
    fig.legend(*ax.get_legend_handles_labels(
        ), loc='upper right', prop={'size': 8})

    return fig
