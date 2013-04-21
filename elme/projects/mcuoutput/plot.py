from __future__ import division
from elme.projects.mcuoutput.analyse import extend
from elme.plotutil import FigureWrapper


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    fw.addcol(legend='out', y=lambda e: e.Aout)
    fw.addcol(legend='amp', y=lambda e: e.Aamp)
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def io_iv_plot(data, fig):
    title = 'Output pin current vs. output voltage (%s)' % (data.model)

    extend(data)
    fw = FigureWrapper(
        data,
        fig,
        y='voltage',
        x='I (mA)',
        title=title)
    y = 'Vout'
    x = 'Iabs'

    fw.addcol(legend='high', x=x, y=y,
              filter_func=lambda e: e.Dout == 1)
    fw.addcol(legend='low', x=x, y=y,
              filter_func=lambda e: e.Dout == 0)
    return fig
