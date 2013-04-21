from __future__ import division
from elme.plotutil import FigureWrapper
from elme.projects.curvetracer.analyse import extend


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    fw.addcol(legend='analog in', y=lambda e: e.Ain)
    fw.addcol(legend='digital in', y=lambda e: e.Din * 1023)
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def dig_input_plot(data, fig):

    title = 'Digital input characteristic %s@%s' % (data.config.pin_dig_in, data.model)

    fw = FigureWrapper(
        data,
        fig,
        x='VCC percentage',
        y='digital in',
        title=title,
        ylimits=[-0.5, 1.5],
    )

    def fperc(e):
        return e.Ain * 100 / 1023

    fw.addcol(legend='up',
              x=fperc,
              y='Din',
              filter_func=lambda e: e.reverse == 0,
              )
    fw.addcol(legend='down',
              x=fperc,
              y='Din',
              filter_func=lambda e: e.reverse == 1,
              )

    return fig
