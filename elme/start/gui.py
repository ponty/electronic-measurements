from entrypoint2 import entrypoint


from elme.gui.plotwnd import PlotWnd


@entrypoint
def main(filename=''):
    gui = PlotWnd()
    gui.configure_traits()
