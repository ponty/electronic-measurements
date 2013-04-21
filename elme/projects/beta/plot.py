from __future__ import division
from elme.formating import format_ohm
from elme.plotutil import FigureWrapper


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    fw.addcol(y='Ab')
    fw.addcol(y='Ac')

    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)




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
##            label='%s rev=%s'%(format_ohm(R), pol)
#            col = dw.col(extract_func=extract_func, filter_func=filter_func)
#            Ax = avg(col)
##            d=col[0]
##            d.middle.analog_value=Ax
#            Rx = calculate_ohm2(R=R, reverse=reverse, A=Ax)
#            print Rx, Ax
#            rr[reverse] = Rx if Rx else 0
#        print sum(rr) / 2
#
#    fw = FigureWrapper(dw, fig, x='time', y='ohm')
#
#    fw.addcol(
#        label='R', extract_func=calculate_ohm)
## fw.addcol(y='high', func=lambda ls:[dw.data.vcc*e for e in ls],
## lineformat='g-o')
#    return fig
