from bunch import Bunch
from entrypoint2 import entrypoint
from traitsui.group import HGroup, Group
from traitsui.item import Item
from traitsui.view import View

from elme.gui.controls import readonly, instance, slider
from elme.gui.mpleditor import MPLFigureEditor
from elme.gui.wnd import AbstractWnd
from elme.projects.scope.measure import measure
from elme.projects.scope.plot import voltage_time_plot
from elme.spectraits import Time, PinTrait
from elme.project import Project


class ScopeWnd(AbstractWnd):
    pin = PinTrait('analog')
    interval = Time()

    @property
    def conf(self):
        return Bunch(pin=self.pin,
                    interval=self.interval)

    def plot(self, data, fig):
        voltage_time_plot(data, fig)

    def measure(self, conf, stop_condition):
        return Project('scope').measure_data(stop_condition)
#         return measure(self.conf, stop_condition)

    view = View(
        HGroup(
            'start',
            'stop',
            'auto_update',
            readonly('alive', checkbox=True),
        ),
#               instance('tester', view=View(
        slider('interval', 0.1, 10),
        'pin',
#                                                         ),
#                    ),
        Group(
        Item('figure',
             editor=MPLFigureEditor(),
             show_label=False
             ),
        ),
        width=600,
        height=300,
        resizable=True)


@entrypoint
def main(filename=''):
    gui = ScopeWnd()
    gui.configure_traits()
