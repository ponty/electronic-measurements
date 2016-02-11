from __future__ import division
from elme.analyse import filter_measurements
from elme.plotutil import FigureWrapper
from elme.util import an2v, pwm2v


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

#     fw.addcol(legend=data.config.pin_in, y='Ain')
#     fw.addcol(legend='%s relativ PWM' % data.config.pin_pwm,
#               y=lambda e: e.pwm_value / 255 * 1023)
    fw.addcol(y='Ain')
    fw.addcol(y='pwm_value')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def transfer_plot(data, fig, error_plot=False):
    data.measurements = filter_measurements(
        data.measurements, ['pwm_value'], ['Ain'])
    title = 'Transfer error plot (%s)' if error_plot else 'Transfer plot (%s)'
    title = title % (data.model)
    fw = FigureWrapper(
        data,
        fig,
        x='voltage',
        y='error (V)' if error_plot else 'voltage',
        title=title,
    )

    vcc = data.vcc
    fw.addcol(legend=data.config.pin_in,
              x=lambda e: pwm2v(e.pwm_value, vcc),
              y=lambda e: an2v(
                  e.Ain, vcc) - (pwm2v(e.pwm_value, vcc) if error_plot else 0),
              )
    ax = fw.subplot
    if error_plot:
        ax.axis([0, 5.1, -0.050, 0.050])

    return fig


def transfer_error_plot(data, fig):
    return transfer_plot(data, fig, error_plot=True)
