from entrypoint2 import entrypoint
from elme.project import Project


@entrypoint
def main(project, plot='analog_value_time_plot', zipfilename=''):
    Project(project).plot(plot).display(zipfilename)
