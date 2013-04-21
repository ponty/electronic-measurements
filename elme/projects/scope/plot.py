from elme.plotutil import FigureWrapper
import logging

log = logging.getLogger(__name__)


def analog_value_time_plot(data, fig, voltage=False):
    fw = FigureWrapper(
        data, fig, x='time', y='analog_value', convert2voltage=voltage)

    legend = data['config']['pin']
    fw.addcol(legend=legend,
              y='A',
              )
    return fig


def voltage_time_plot(data, fig):
    return analog_value_time_plot(data, fig, voltage=True)
