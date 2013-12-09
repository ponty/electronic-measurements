from __future__ import division
from elme.plotutil import FigureWrapper


def frequency_time_plot(data, fig):
    fw = FigureWrapper(
        data, 
        fig, 
        x='time', 
        y='frequency',
        draw_axis=False)

    fw.addcol(y='frequency')
#     fw.subplot.set_ylim(bottom=100000)
#     fw.subplot.set_ylim(auto=True)
#     ax = fw.subplot
#     ax.set_autoscale_on(True)
#     ax.autoscale_view(True,False,True)
    return fig



