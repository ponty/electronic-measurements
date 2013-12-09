'''
doc generator with cog
'''

from elme.project import Project
from path import path


def schematic(cog, projname):
    cog.outl()
    cog.outl('Schematic::')
    cog.outl()
    cog.outl(Project(projname).schematic.text)
    
# def schematic_template(cog, projname):
#     cog.outl()
#     cog.outl('Schematic template::')
#     cog.outl()
#     cog.outl(Project(projname).schematic.template)
# 
# def schematic_all(cog, projname):
#     schematic_template(cog, projname)
#     schematic(cog, projname)
    

TIMEPLOT = 'analog_value_time_plot'


def plots(cog, projname, plot_types=[], auto_time_plot=True):
    if auto_time_plot and TIMEPLOT not in plot_types:
        plot_types += [TIMEPLOT]
    d = path('docs/data/' + projname)
    if not d.exists():
        print 'missing directory:%s' % d
        return
    for plot_type in plot_types:
        cog.outl()
        cog.outl(plot_type.replace('_', ' '))
        cog.outl('------------------------------')
        cog.outl()
        for f in sorted(d.files()):
            cog.outl()
            cog.outl(f.namebase.replace('_', ' '))
            cog.outl('++++++++++++++++++++++++++++++++++')
            cog.outl()
            cog.outl('.. plot::')
            cog.outl()
            cog.outl('    from elme.project import Project')
            options = dict(proj=projname,
                           plot=plot_type,
                           f=f.partition('/')[2],  # remove root dir
                           #                     dir=d,
                           )
            cog.outl("    Project('{proj}').plot('{plot}').embed('{f}')".format(**options))

#        cog.outl('    from elme.swing.plot import *')
#        cog.outl('    from elme.plotutil import plot_any')
#        cog.outl('    f="/%s"' % f)
#        cog.outl('    plot_any(time_plot, f)')
#        cog.outl('    plot_any(input_range_plot, f)')
#        cog.outl('    plot_any(output_swing_plot, f)')
            cog.outl()
