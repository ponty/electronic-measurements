from __future__ import division
from bunch import bunchify
from elme.formating import format_ohm
from elme.plotutil import FigureWrapper
from elme.projects.lcmeter.analyse import analyse, process


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    fw.addcol(legend='top', y=lambda e: e.get('Atop'))
    fw.addcol(legend='middle', y=lambda e: e.get('Amiddle'))
    fw.addcol(legend='bottom', y=lambda e: e.get('Abottom'))

    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)


def processed_plot(dw, fig):
    d = process(dw)

    d = bunchify(d)
    newdata = dict(measurements=d, project='esr')

    fw = FigureWrapper(
        newdata, fig, x='frequency', y='R',
        ylimits=[0, 1023],
    )

    for top in dw.data.config.toplist:
        fw.addcol(y='Amin', filter_func=lambda e: e.R == top.R)
        fw.addcol(y='Amax', filter_func=lambda e: e.R == top.R)
        fw.addcol(y='Aavg', filter_func=lambda e: e.R == top.R)
        fw.addcol(y='Arange', filter_func=lambda e: e.R == top.R)

    ax = fw.subplot
    ax.set_xscale('log')
    # ax.set_yscale('log')

    return fig


# def calculate_ohm(d):
#    reverse = (d.top == 0 and d.bottom == 1)
#    Ax = d.middle
#    R = d.R
#    return calculate_ohm2(R=R, reverse=reverse, A=Ax)


# def avg(ls):
#    # median(ls)
#    drop = 0.4
#    istart = int(len(ls) * drop / 2)
#    istop = len(ls) - istart
#    ls2 = sorted(ls)[istart:istop + 1]
#    return sum(ls2) / len(ls2)
#
#
# def ohm_time_plot(dw, fig):
#    for h in dw.data.config.toplist:
#        rr = [0, 0]
#        for reverse in [0, 1]:
#            R = h.R
#            extract_func = lambda e: e.middle
#            filter_func = lambda e: e.R == R and e.bottom == reverse
# #            label='%s rev=%s'%(format_ohm(R), pol)
#            col = dw.col(extract_func=extract_func, filter_func=filter_func)
#            Ax = avg(col)
# #            d=col[0]
# #            d.middle.analog_value=Ax
#            Rx = calculate_ohm2(R=R, reverse=reverse, A=Ax)
#            print Rx, Ax
#            rr[reverse] = Rx if Rx else 0
#        print sum(rr) / 2
#
#    fw = FigureWrapper(dw, fig, x='time', y='ohm')
#
#    fw.addcol(
#        label='R', extract_func=calculate_ohm)
# # fw.addcol(y='high', func=lambda ls:[dw.data.vcc*e for e in ls],
# # lineformat='g-o')
#    return fig
def plotx(dw, fig, name, ylabel, log_y_axis=True):
    d = process(dw)
    d = bunchify(d)
    newdata = dict(measurements=d, project='esr')
    fw = FigureWrapper(
        newdata, fig, x='frequency', y=ylabel,
        log_x_axis=True,
        log_y_axis=log_y_axis,
    )
    for top in dw.data.config.toplist:
        fw.addcol(y=name, filter_func=lambda e: e.R == top.R)

    return fig


def ohm_plot(dw, fig):
    return plotx(dw, fig, 'Rx', log_y_axis=True, ylabel='ohm')


def cap_plot(dw, fig):
    return plotx(dw, fig, 'Cx', log_y_axis=False, ylabel='farad')


def ind_plot(dw, fig):
    return plotx(dw, fig, 'Lx', log_y_axis=False, ylabel='henry')
