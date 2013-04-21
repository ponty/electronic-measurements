from __future__ import division
from elme.projects.curvetracer.analyse import extend
from elme.plotutil import FigureWrapper


# def time_plot(data, fig):
#    dw = DataWrapper(data)
#    dw.calculate_trel()
#    title = 'Time plot'
#
#    ax = fig.add_subplot(111, title=title)
#    ax.plot(dw.col('trel'), dw.col('Vin'), 'g-o', label='Vin')
#    ax.plot(dw.col('trel'), dw.col('Vout'), 'b-o', label='Vout')
#    ax.plot(dw.col('trel'), dw.col('Vamp'), 'r-o', label='Vamp')
#
#    ax.set_ylabel('V (V)')
#    ax.set_xlabel('t (sec)')
#
#    ax.grid(True)
#
#    fig.legend(*ax.get_legend_handles_labels(), loc='upper right')
#
#    ax.xaxis.set_major_locator(MultipleLocator(1))
#    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
#
#    ax.yaxis.set_major_locator(MultipleLocator(1))
#    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
#
#    return fig

def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

#    fw.addcol(legend='rel pwm', y=lambda e: e.pwm_value/255*1023)
    fw.addcol(legend='in', y=lambda e: e.Ain)
    fw.addcol(legend='out', y=lambda e: e.Aout)
    fw.addcol(legend='amp', y=lambda e: e.Aamp)
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def processed_analog_value_time_plot(data, fig):
    fw = FigureWrapper(
        data, fig, x='time', y='voltage')

    extend(data)

#    fw.addcol(legend='rel pwm', y=lambda e: e.pwm_value/255*1023)
    fw.addcol(legend='Vin', y=lambda e: e.Vin)
    fw.addcol(legend='Vout', y=lambda e: e.Vout)
    fw.addcol(legend='Vamp', y=lambda e: e.Vamp)
    fw.addcol(legend='Vx', y=lambda e: e.Vx)
    fw.addcol(legend='I', y=lambda e: e.I)
    return fig


def IV_curve_plot(data, fig):
    title = 'I/O pin current vs. output voltage'
    extend(data)
    fw = FigureWrapper(
        data,
        fig,
        x='voltage',
        y='I (A)',
        title=title,
        xlimits=[-5, 5],
        ylimits=[-0.020, 0.020],
    )

    x = 'Vx'
    y = 'I'

    fw.subplot.plot(
        [0, data.Vmax],
        [data.Imax, 0],
        'b-')
    fw.subplot.plot(
        [0, -data.Vmax],
        [-data.Imax, 0],
        'b-')

    fw.addcol(legend='', x=x, y=y)

    return fig
