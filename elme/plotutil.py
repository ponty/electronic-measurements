from decotrace import traced
from matplotlib.ticker import AutoMinorLocator
from softusbduino.util import an2v
from uncertainties.unumpy.core import nominal_values
import matplotlib


class FigureWrapper(object):
    def __init__(self, data, figure, x=None, y=None, title=None, xlimits=None,
                 ylimits=None,
                 convert2voltage=False,
                 log_x_axis=False,
                 log_y_axis=False,
                 ):
        self.data = data
        self.convert2voltage = convert2voltage
        self.x = x
        self.y = y

        if self.convert2voltage and self.y == 'analog_value':
            y = 'voltage'
#        dw = DataWrapper(data)
#        dw.calculate_trel()
#        self.datawrapper = dw
        fig = self.figure = figure
        ax = self.subplot = figure.add_subplot(111)
        if x == 'time':
            if not title:
                title = 'Time plot'
            ax.set_xlabel('t (sec)')

        def axislabel(e):
            if e == 'voltage':
                e = 'Voltage (V)'
            if e == 'analog_value':
                e = 'Analog value'
            if not e:
                e = ''
            return e

        ax.set_xlabel(axislabel(x))
        ax.set_ylabel(axislabel(y))
        if title:
            ax.set_title(title)

        ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        ax.yaxis.set_minor_locator(AutoMinorLocator(10))

        ax.grid(True)

        ax.grid(True, which='major', linestyle='-', color='grey')
        ax.grid(True, which='minor', linestyle='-', color='lightgrey')

        if log_x_axis:
            ax.set_xscale('log')
        if log_y_axis:
            ax.set_yscale('log')
        if not log_x_axis and not log_y_axis:
            ax.axvline(x=0, color='black')  # not recommended for log axis
            ax.axhline(y=0, color='black')  # not recommended for log axis

        if not ylimits:
            if y == 'analog_value':
                ylimits = [0, 1023]
            if y == 'voltage':
                ylimits = [0, self.data['vcc']]
        if ylimits:
            ax.axhline(y=ylimits[0], color='black')
            ax.axhline(y=ylimits[1], color='black')
            ax.set_ylim(ylimits)

        if not xlimits:
            if x == 'analog_value':
                xlimits = [0, 1023]
            if x == 'voltage':
                xlimits = [0, data['vcc']]
        if xlimits:
            ax.axvline(x=xlimits[0], color='black')
            ax.axvline(x=xlimits[1], color='black')
            ax.set_xlim(xlimits)

        # disable offset on axis
        formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)

    def update_legend(self):
        fig = self.figure
        ax = self.subplot
        fig.legend(*ax.get_legend_handles_labels(
        ), loc='upper right', prop={'size': 8})

    def _col(self, key, filter_func=None):
        assert key
        df = self.data['measurements']
        if filter_func:
            df = df[filter_func(df)]

        if callable(key):
            return key(df)
#            return [key(r) for r in self.data['measurements']
#                    if not filter_func or filter_func(r)]
        else:
            return df[key]
#            return [r[key] for r in self.data['measurements']
#                    if not filter_func or filter_func(r)]

    def addcol(self, x=None, y=None, legend=None, lineformat=None, filter_func=None, sortbyx=None):
#        dw = self.datawrapper
        ax = self.subplot
        if x and not callable(x):
            ax.set_xlabel(x)
        else:
            if self.x == 'time':
                x = 't'
        if not x:
            x = self.x

        if not lineformat:
            lineformat = '-o'

#        f1 = y
        if not callable(y):
            if not legend:
                legend = y

        if self.convert2voltage and self.y == 'analog_value':
            f2 = lambda e: an2v(e[y], self.data['vcc'])
        else:
            f2 = y

        xcol = self._col(x, filter_func=filter_func)
        ycol = self._col(f2, filter_func=filter_func)
        if sortbyx:
            ls = sorted(zip(xcol, ycol), key=lambda e: e[0])
            xcol = [e[0] for e in ls]
            ycol = [e[1] for e in ls]
#        print 888,xcol
#        print 888,ycol
        assert len(xcol) == len(ycol)
        assert len(xcol)
        assert len(ycol)
        ax.plot(
            nominal_values(xcol),
            nominal_values(ycol),
            #            [func(e) for e in dw.data.measurements],
            lineformat,
            label=legend)
        self.update_legend()
