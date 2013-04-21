from elme.gui.controls import readonly, instance, slider
from elme.gui.mpleditor import MPLFigureEditor
from elme.projects.scope.measure import measure
from elme.spectraits import Time, PinTrait
from elme.gui.wnd import AbstractWnd
from traitsui.group import HGroup, Group
from traitsui.item import Item
from traitsui.view import View


class ScopeWnd(AbstractWnd):
    pin = PinTrait('analog')
    interval = Time()

    @property
    def conf(self):
        return dict(pin=self.pin,
                    interval=self.interval)

    def plot(self, data, fig):
        time_plot(data, fig)

    def measure(self, conf, stop_condition):
        return measure(self.conf, stop_condition)

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
