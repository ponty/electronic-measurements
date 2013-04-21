from entrypoint2 import entrypoint
from elme.gui.plotwnd import PlotWnd
import cProfile
import pstats


@entrypoint
def main():
    cProfile.run('PlotWnd().configure_traits()', 'fooprof')
    p = pstats.Stats('fooprof')
    p.sort_stats('time').print_stats(50)
