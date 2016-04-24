from __future__ import division
from elme.analyse import filter_measurements
from elme.plotutil import FigureWrapper
from elme.util import an2v


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

#     fw.addcol(legend=data.config.pin_in, y='Ain')
#     fw.addcol(legend='%s relativ PWM' % data.config.pin_pwm,
#               y=lambda e: e.value / 255 * 1023)
    fw.addcol(y='Ain')
    fw.addcol(y='value')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def pot2v(value, vcc):
    #     return (value - 1) / 98 * vcc
    return value / 99 * vcc


def transfer_plot(data, fig, error_plot=False):
    data.measurements = filter_measurements(
        data.measurements, ['value'], ['Ain'])
    title = 'Transfer error plot' if error_plot else 'Transfer plot'
    title = title
    fw = FigureWrapper(
        data,
        fig,
        x='voltage',
        y='error (V)' if error_plot else 'voltage',
        title=title,
    )

    vcc = data.vcc

    if error_plot:
        fw.subplot.plot(
            [0, vcc],
            [vcc / 99, vcc / 99],
            'r-')
        fw.subplot.plot(
            [0, vcc],
            [-vcc / 99, -vcc / 99],
            'r-')
    else:
        fw.subplot.plot(
            [0, 0],
            [vcc, vcc],
            'r-')

    fw.addcol(legend=data.config.pin_in,
              x=lambda e: pot2v(e.value, vcc),
              y=lambda e: an2v(
                  e.Ain, vcc) - (pot2v(e.value, vcc) if error_plot else 0),
              )
    ax = fw.subplot
    if error_plot:
        ax.axis([0, 5.1, -0.1, 0.1])

    return fig


def transfer_error_plot(data, fig):
    return transfer_plot(data, fig, error_plot=True)
