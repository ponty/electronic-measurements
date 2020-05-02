from bunch import Bunch
from entrypoint2 import entrypoint
from time import sleep
from traits.trait_types import Int, Instance, Float, Bool
from traitsui.group import HGroup, Group, VGroup
from traitsui.item import Item
from traitsui.view import View

from elme.gui.controls import readonly, slider
from elme.gui.mpleditor import MPLFigureEditor
from elme.gui.wnd import AbstractWnd
from elme.project import Project
from elme.projects.load.analyse import calc_Vin, calc_Iin
from elme.projects.load.measure import Hardware
from elme.spectraits import Time, PinTrait, UVoltage


class LoadWnd(AbstractWnd):
#     pin = PinTrait('analog')
    interval = Time()
    mask1 = Int(0)
    mask2 = Int(0)
    mask_index = Int(1)
    hw = Instance(Hardware)
    vcc = Float()
    Ain = Float()
    volt = Float()
    Ahall = Float()
    amper = Float()
    volt_division = Float(5.624)
    hall_VperA = Float(0.066)
    watt = Float()
    ohm = Float()
    ohm_nominal = Float()
    Vdiv = Float()
    alternate = Bool(False)
    
    def _hw_default(self):
        project = Project.find('load')
        hw = Hardware(project.config)
        return hw
        
    def _mask1_changed(self):
        if not self.alternate:
            self.hw.set_r_mask(self.mask1)
        
    @property
    def conf(self):
        return Bunch(interval=self.interval)

    def plot(self, data, fig):
        pass
#         voltage_time_plot(data, fig)

    def measure(self, conf, stop_condition):
#         return Project('scope').measure_data(stop_condition)
#         return measure(self.conf, stop_condition)
        self.Ain = self.hw.read_Ain()
        self.Ahall = self.hw.read_Ahall()
        
        vcc = 4.796  # 4.688  # self.hw.read_Vcc()
        self.vcc = vcc
#         print 4.688*201/1024*5.56
        self.volt = calc_Vin(self.Ain, vcc, self.volt_division)
        self.Vdiv = self.volt / self.volt_division
        self.amper = calc_Iin(self.Ahall, vcc, self.hall_VperA)
        self.watt = self.volt * self.amper
        self.ohm = self.volt / self.amper if self.amper > 0 else -1
        if self.alternate:
            self.mask_index += 1
            if self.mask_index > 2:
                self.mask_index = 1

            if self.mask_index == 1:
                self.hw.set_r_mask(self.mask1)
                self.ohm_nominal = self.hw.get_r_mask_ohm(self.mask1)
            else:
                self.hw.set_r_mask(self.mask2)
                self.ohm_nominal = self.hw.get_r_mask_ohm(self.mask2)
        else:
            self.ohm_nominal = self.hw.get_r_mask_ohm(self.mask1)
            
        sleep(self.interval)
        
    view = View(
        HGroup(
            'start',
            'stop',
            'auto_update',
            readonly('alive', checkbox=True),
        ),
#               instance('tester', view=View(
        slider('interval', 0.1, 10),
        slider('mask1', 0, 255, is_float=False),
        slider('mask2', 0, 255, is_float=False),
        'alternate',
        HGroup(
            VGroup(
        readonly('volt', format_str='%01.1f V'),
        readonly('amper', format_str='%01.1f A'),
        readonly('watt', format_str='%01.1f W'),
        readonly('ohm', format_str='%01.2f Ohm'),
        readonly('ohm_nominal', format_str='%01.2f Ohm'),
                ),
            VGroup(
        readonly('Ain', format_str='%d'),
        readonly('Ahall', format_str='%d'),
        readonly('Vdiv', format_str='%01.3f V'),
        readonly('vcc', format_str='%01.3f V'),
                ),
            ),
        
#         'pin',
#                                                         ),
#                    ),
#         Group(
#         Item('figure',
#              editor=MPLFigureEditor(),
#              show_label=False
#              ),
#         ),
        width=600,
        height=300,
        resizable=True)


@entrypoint
def main(filename=''):
    gui = LoadWnd()
    gui.configure_traits()
