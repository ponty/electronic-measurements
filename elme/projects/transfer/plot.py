from __future__ import division
from elme.projects.transfer.analyse import extend
from elme.plotutil import FigureWrapper


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

#    fw.addcol(legend='rel pwm', y=lambda e: e.pwm_value/255*1023)
    fw.addcol(legend='in', y='Ain')
    fw.addcol(legend='out', y='Aout')
    fw.addcol(legend='amp', y='Aamp')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def processed_analog_value_time_plot(data, fig):
    fw = FigureWrapper(
        data, fig, x='time', y='voltage')

    extend(data)

    fw.addcol(legend='Vin', y='Vin')
    fw.addcol(legend='Vout', y='Vout')
    fw.addcol(legend='Vamp', y='Vamp')
    return fig


def transfer_plot(data, fig):
    title = 'Voltage Transfer Curve'
    extend(data)
    fw = FigureWrapper(
        data,
        fig,
        x='Vin (V)',
        y='Vout (V)',
        title=title,
#        xlimits=[-5, 5],
#        ylimits=[-0.020, 0.020],
    )

    fw.subplot.plot(
        [0, data.Vmax],
        [0, data.Vmax],
        'r-')
    fw.subplot.plot(
        [0, data.Vmax],
        [data.Vmax, 0],
        'r-')

#     fw.addcol(legend='', x='Vin', y='Vout')
    fw.addcol(legend='up',
              x='Vin',
              y='Vout',
              filter_func=lambda e: e.reverse == 0,
              )
    fw.addcol(legend='down',
              x='Vin',
              y='Vout',
              filter_func=lambda e: e.reverse == 1,
              )

    return fig
