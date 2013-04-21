from __future__ import division
from numpy.ma.core import logical_and
from elme.formating import format_ohm
from elme.plotutil import FigureWrapper
from elme.projects.swing.analyse import calculate_good_interval, extend, \
    NO_LOAD


def get_filter_func(R, phase):
        def filter_func(x):
            ok = logical_and(x.Rload == R, x.phase == phase)
#            print 334,x,R, phase
#            print ok
            return ok
        return filter_func


def Rloads(data):
    ls = list(set(data.measurements['Rload']))
    ls.sort()
    return ls


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    fw.addcol(legend='plus', y='Aplus')
    fw.addcol(legend='minus', y='Aminus')
    fw.addcol(legend='out', y='Aout')
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def unity_gain_plot(data, fig, error_plot=False):
#    dw = DataWrapper(data)
    config = data.config
    vcc = data.vcc
    measurements = data.measurements
#    A = config.R2 / config.R1

    extend(data)
    fw = FigureWrapper(
        data, fig,
        x='voltage',
        y='error' if error_plot else 'voltage',
        title='Unity gain')

#    ax = fig.add_subplot(111)

    yname = 'Vout_diff' if error_plot else 'Vout'
    for R in [NO_LOAD]:
        fw.addcol(legend='',
                  x='Vout_expected',
                  y=yname,
                  filter_func=get_filter_func(R, 'unity_gain'),
                          )
    ax = fw.subplot
    ax.set_xlabel('Vout_expected (V)')
#    ax.grid(True)
#    ax.axvline(x=0, color='black')
#    ax.axvline(x=dw.data.vcc, color='black')
    if error_plot:
        limit = 0.050
        ax.axhline(y=limit, color='red')
        ax.axhline(y=-limit, color='red')

        # TODO: vlines
#         interv = calculate_good_interval(config, measurements, limit=limit)
#         if interv:
#             ax.axvline(x=interv[0], color='red')
#             ax.axvline(x=interv[1], color='red')

        ax.axhline(y=0, color='black')
        ax.set_ylabel('error (V)')
#        ax.axis([0, 5.1, -0.5, 0.5])
    else:
        ax.plot([0, vcc], [0, vcc])
#        ax.axis([0, 5.1, 0, 5.1])
        ax.set_ylabel('Vout (V)')

    return fig


def unity_gain_error_plot(data, fig):
    return unity_gain_plot(data, fig, error_plot=True)


def output_swing_plot(data, fig, error_plot=False):
    vcc = data.vcc
    extend(data)
    fw = FigureWrapper(
        data, fig,
        x='voltage',
        y='error' if error_plot else 'voltage',
        title='Maximum peak output voltage swing')
    yname = 'Vout_diff' if error_plot else 'Vout'
    for R in Rloads(data):
        fw.addcol(legend=unicode(format_ohm(R) if R else R),
                  x='Vout_expected',
                  y=yname,
                  filter_func=get_filter_func(R, 'output_swing'),
                  sortbyx=True,
                          )

    ax = fw.subplot
#    ax.legend(*ax.get_legend_handles_labels(), loc='upper center')
    ax.set_xlabel('Expected (V)')

#    ax.grid(True)
#    ax.axvline(x=0, color='black')
#    ax.axvline(x=dw.data.vcc, color='black')
#    ax.axhline(y=0, color='black')
    if error_plot:
        ax.set_ylabel('error (V)')
#        ax.axis([0, 5.1, -0.2, 0.2])
    else:
#        ax.axhline(y=dw.data.vcc, color='black')
        ax.plot([0, vcc], [0, vcc])
#        ax.axis([0, 5.1, 0, 5.1])
        ax.set_ylabel('Real (V)')
    return fig


def output_swing_error_plot(data, fig):
    return output_swing_plot(data, fig, error_plot=True)


def input_range_plot(data, fig, error_plot=False):
    vcc = data.vcc

    extend(data)
    fw = FigureWrapper(
        data,
        fig,
        x='voltage',
        y='error' if error_plot else 'voltage',
        title='Common-mode input voltage range')
#    print data.measurements

    yname = 'Vin_diff' if error_plot else 'Vopamp_minus'
    for R in [NO_LOAD]:
        fw.addcol(legend='',
                  x='Vplus',
                  y=yname,
                  filter_func=get_filter_func(R, 'input_range'),
                          )

    ax = fw.subplot
    ax.set_xlabel('opamp+ (V)')

#    ax.grid(True)
#    ax.axvline(x=0, color='black')
#    ax.axvline(x=dw.data.vcc, color='black')
    if error_plot:
#        ax.axhline(y=0, color='black')
        ax.set_ylabel('error (V)')
#        ax.axis([0, 5.1, -0.050, 0.050])
    else:
        ax.plot([0, vcc], [0, vcc])
#        ax.axis([0, 5.1, 0, 5.1])
        ax.set_ylabel('opamp- (V)')
    return fig


def input_range_error_plot(data, fig):
    return input_range_plot(data, fig, error_plot=True)
