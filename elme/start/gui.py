from entrypoint2 import entrypoint
import logging

from elme.gui.plotwnd import PlotWnd


# logging.basicConfig(level=logging.DEBUG)

@entrypoint
def main(filename=''):
    gui = PlotWnd()
    gui.configure_traits()
