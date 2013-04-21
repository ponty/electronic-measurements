from configobj import ConfigObj
from path import path
from elme.gui.controls import readonly, button
from elme.gui.inputbox import inputbox
from elme.gui.mpleditor import MPLFigureEditor
from elme.gui.textbox import textbox
from elme.gui.wnd import FigureWnd
from elme.project import Project
from elme.util import tmpdir
from traits.trait_types import Any, Enum, CSet, List, Button
from traitsui.editors.enum_editor import EnumEditor
from traitsui.group import HGroup, Group
from traitsui.item import Item
from traitsui.message import message
from traitsui.view import View
from zipfile import ZipFile
import tempfile
import traceback
import webbrowser


projects = Project.all()
HOME_DIR = path('~').expanduser() / ".measurements"


def open_text_file_in_editor(file_path):
    webbrowser.open_new_tab(file_path)
#        os.system('gnome-open '+file_path)


def open_string_in_editor(s):
    file_out = tempfile.NamedTemporaryFile(
        prefix='measurement_', suffix='', delete=0)
    file_out.close()
    path(file_out.name).write_text(s)
    open_text_file_in_editor(file_out.name)


class ConfigFile(object):
    filename = HOME_DIR / 'plotwnd.ini'

    def __init__(self):
        self.configobj = ConfigObj(self.filename)

#    @traced
    def get(self, key):
        return self.configobj.get(key)

#    @traced
    def set(self, key, value):
        self.configobj[key] = value
        self.configobj.write()
# def names(objs):
#    return [x.name for x in objs]


class PlotWnd(FigureWnd):
    dummy = Any

    def _dummy_default(self):
        self._project_changed()

    configfile = ConfigFile()
#    conf = None
    project = Enum(projects)

    def mfullpath(self, m):
        return self.project.result_dir / m

    def _project_default(self):
        x = Project.find(self.configfile.get('project'))
        if x:
            return x
        else:
            return projects[-1]

    plot_type = Any

    def _plot_type_default(self):
        x = self.project.plot(self.configfile.get('plot_type'))
        if x:
            return x
        else:
            if len(self.available_plots):
                return self.available_plots[-1]

    available_plots = List()

    def _available_plots_default(self):
        return self.project.allplots()

    measurement = Any
    available_measurements = List()

    def _available_measurements_default(self):
        return self.project.allmeasurements()

#    @traced
    def _measurement_changed(self):
        self.update_figure()

    def _plot_type_changed(self):
        self.update_figure()
        if self.plot_type:
            self.configfile.set('plot_type', self.plot_type.name)

    def _available_plots_changed(self):
        if len(self.available_plots):
            self.plot_type = self.available_plots[0]

#    @traced
    def update_available_measurements(self):
        def fnames(ls):
            return [x.name for x in ls]
        self.available_measurements = fnames(self.project.allmeasurements())
        if len(self.available_measurements):
            self.measurement = self.available_measurements[-1]
        else:
            self.measurement = None
#        self.measurement = None

    def _project_changed(self):
        self.configfile.set('project', self.project.name)

#        self.plot_type = None
#        self.available_plots = []
#        self.measurement = None
#        self.available_measurements = []
        self.update_available_measurements()
        self.available_plots = self.project.allplots()
#        if len(self.available_plots):
#            self.plot_type = self.available_plots[0]

    def create_plot(self, fig):
#        dw = DataWrapper(zipfile=self.measurement)
        try:
            assert self.measurement
            self.plot_type.create(fig, self.mfullpath(self.measurement))
        except Exception as e:
            traceback.print_exc()

#    def measure(self, conf, stop_condition):
#        self.project.measure()
    reload = Button()

    def _reload_fired(self):
        self.update_available_measurements()

    show = Button()

    def _show_fired(self):
        assert self.measurement
#        dw = DataWrapper(zipfile=self.mfullpath(self.measurement))
#        file_out = tempfile.NamedTemporaryFile(
#            prefix='measurement_', suffix='.json', delete=0)
#        file_out.close()
#        self.project.save(file_out.name, as_zip=0)
        d = tmpdir()
        z = ZipFile(self.mfullpath(self.measurement))

        z.extractall(d)
        for f in d.walkfiles():
            print f
            open_text_file_in_editor(f)

    rename = Button()

    def _rename_fired(self):
        assert self.measurement
        newname = inputbox(message='new name:',
                           default=self.measurement)
        if newname:
            (self.project.result_dir /
             self.measurement).rename(self.project.result_dir / newname)
            self.update_available_measurements()

    delete = Button()

    def _delete_fired(self):
        assert self.measurement
        res = message(
            'Delete "%s" ?' % self.measurement, buttons=['OK', 'Cancel'])
        if res:
#            path
            (self.project.result_dir / self.measurement).remove()
            self.update_available_measurements()

    directory = Button()

    def _directory_fired(self):
        open_text_file_in_editor(self.project.result_dir)

    analyse = Button()

    def _analyse_fired(self):
        assert self.measurement
        s = self.project.analyse_str(self.mfullpath(self.measurement))
        print(s)
        textbox(s)

    open = Button()

    def _open_fired(self):
#        print self.measurement
        assert self.measurement
# show.show(self.project.name, self.plot_type.name, self.measurement,
# block=False)
        self.plot_type.display(self.mfullpath(self.measurement), block=False)

    config = Button()

    def _config_fired(self):
        open_text_file_in_editor(self.project.default_config_path)

    schematic_template = Button()

    def _schematic_template_fired(self):
        open_text_file_in_editor(self.project.schematic.template_path)

    schematic = Button()

    def _schematic_fired(self):
        open_string_in_editor(self.project.schematic.text)
    measure = Button()

    def _measure_fired(self):
#        print self.project.schematic.text
#        print self.project.default_config

        self.project.measure()
        self.update_available_measurements()

#        print self.available_plots
#        data = analyse(data)
#        IV_curve_plot(data, fig)
#    def measure(self, conf, stop_condition):
#        data = measure(self.conf)
#        return data
    view = View(
        Group(
            Item(name='dummy',
                 defined_when='0'
                 ),
            HGroup(
                'project',
                button('config'),
                button('schematic_template'),
                button('schematic'),
                button('measure'),
            ),
            HGroup(
                Item(name='measurement',
                     editor=EnumEditor(
                     name='available_measurements'
                     ),
                     #                     style='custom',
                     ),
                button('reload'),
                button('show'),
                button('directory'),
                button('analyse'),
                button('rename'),
                button('delete'),

            ),
            HGroup(
                Item(name='plot_type',
                     editor=EnumEditor(
                     name='available_plots'
                     ),
                     #                     style='custom',
                     ),
                button('open'),
            ),

#            'start',
#            'stop',
#            'auto_update',
#            readonly('alive', checkbox=True),

        ),
        '_',
        Group(
        Item('figure',
             editor=MPLFigureEditor(),
             show_label=False
             ),
        ),
        width=900,
        height=600,
        resizable=True)
