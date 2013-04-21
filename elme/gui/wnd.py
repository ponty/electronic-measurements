from matplotlib.figure import Figure
from threading import Thread
from traits.has_traits import HasTraits
from traits.trait_types import Float, Instance, Button, Bool, Any


class FigureWnd (HasTraits):
    figure = Instance(Figure)

    def _figure_default(self):
        pass

    def update_figure(self):
        fig = Figure()
        self.create_plot(fig)
        self.figure = fig


class AbstractWnd (HasTraits):
    figure = Instance(Figure)

    def _figure_default(self):
        pass

    alive = Bool()
    auto_update = Bool(False)
    enable_update = Bool()
    start = Button()

    def _start_fired(self):
        self.enable_update = True
        Thread(target=self._loop).start()

    stop = Button()

    def _stop_fired(self):
        self.enable_update = False

    def _loop(self):
        if self.auto_update:
            while self.auto_update and self.enable_update:
                self._update()
        else:
            self._update()

    def _update(self):
        self.alive = True

        def stop_condition(t, tstart):
            return not self.enable_update

        data = self.measure(self.conf, stop_condition)
        self.alive = False

        fig = Figure()
        self.plot(data, fig)
        self.figure = fig
