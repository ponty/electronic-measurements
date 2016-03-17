from __future__ import division
from copy import copy
from elme.plotutil import FigureWrapper
from elme.projects.acvoltmeter.analyse import analyse
import numpy as np


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(data, fig, x='time', y='analog_value',
                       convert2voltage=voltage)

    fw.addcol(legend='volt', y='Avolt')
    fw.addcol(legend='current', y='Acurrent')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


