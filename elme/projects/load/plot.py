from __future__ import division

from elme.plotutil import FigureWrapper
from elme.projects.load.analyse import extend


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(data, fig, x='time', y='analog_value',
                       convert2voltage=voltage)

    fw.addcol(legend='volt', y='Ain')
    fw.addcol(legend='current', y='Ahall')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def VI_curve_plot(data, fig):
    title = 'output voltage vs. output current'
    extend(data)
    fw = FigureWrapper(
        data,
        fig,
        x='I (A)',
        y='voltage',
        title=title,
#         xlimits=[0, 10],
        ylimits=[0, 6],
    )

    x = 'Iin'
    y = 'Vin'

#     Vmax=6
#     Imax=10
#     fw.subplot.plot(
#         [0, Vmax],
#         [Imax, 0],
#         'b-')
#     fw.subplot.plot(
#         [0, -data.Vmax],
#         [-data.Imax, 0],
#         'b-')

    fw.addcol(legend='', x=x, y=y)

    return fig
