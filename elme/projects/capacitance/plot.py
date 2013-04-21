from __future__ import division
from elme.plotutil import FigureWrapper


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

#    fw.addcol(legend='top', y='Atop')
    fw.addcol(legend='middle', y='Amiddle')
#    fw.addcol(legend='bottom', y='Abottom')

    return fw


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def voltage_time_log_plot(data, fig):
    fw = analog_value_time_plot(data, fig, voltage=True)
    fw.subplot.set_yscale('log')
