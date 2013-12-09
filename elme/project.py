from __future__ import division
from StringIO import StringIO
from bunch import bunchify, unbunchify
from decotrace import traced
from easyprocess import EasyProcess
from elme import dumper
from path import path
from prettyprint.prettyprint import pp_str
from softusbduino.memo import memoized
from zipfile import ZipFile, ZIP_DEFLATED
import datetime
import importlib
import matplotlib.pyplot as plt
import pandas as pd
import sys
import time

root = path(__file__).parent

DEFAULT_CONFIG_JSON = 'default_config.yaml'
HOME_DIR = path('~').expanduser() / ".measurements"
PROJECTS_MODULE = 'elme.projects'
PROJECTS_HOME = root / 'projects'
SCHEMATIC_TEMPLATE_NAME = 'schematic.txt'


# def wrapcli(zipfilename, project):
#    if not zipfilename:
#        dw = CDataWrapper.latest(project)
#    else:
#        dw = CDataWrapper(zipfile=zipfilename)
#    return dw


def format_time(i=None):
    return time.strftime('%Y.%m.%d__%H_%M_%S', time.localtime(i))

# class CDataWrapper(object):
#    def __init__(self, data=None, zipfile=None, project=None):
#        assert 0
#        if isinstance(data, CDataWrapper):
#            self.data = data.data
#        else:
#            self.data = bunchify(data)
#        if project:
#            self.project = project
#        else:
#            if self.data:
#                self.project = self.data.project
#        if zipfile:
#            self.load(zipfile)
#    @classmethod
#    def latest(cls, project):
#        d = project.result_dir
#        ls = sorted(d.files(), key=lambda r: r.ctime)
#
#        zipfilename = ls[-1]  # last
#        return CDataWrapper(zipfile=zipfilename, project=project)
#    @classmethod
#    def files(cls, project):
#        d = project.result_dir
#        ls = sorted(d.files(), key=lambda r: r.ctime)
#        return ls
#    def auto_name(self):
#        name = '%s_%s' % (self.project,format_time())
#    #    name = name.replace(" ", '_')
##        self.result_dir.makedirs_p()
#        return self.result_dir / name
#    def col(self, key, filter_func=None):
#        assert key
#        if callable(key):
#            return [key(r) for r in self.data['measurements']
#                    if not filter_func or filter_func(r)]
#        else:
#            return [r[key] for r in self.data['measurements']
#                    if not filter_func or filter_func(r)]
#    def cols4plot(self, xname, yname, filter_func=None, median_filters=[]):
#        ls = [r for r in self.data['measurements']
#              if not filter_func or filter_func(r)]
#        ls.sort(key=lambda r: r[xname])
#        xcol = [r[xname] for r in ls]
#        ycol = [r[yname] for r in ls]
#
#        def _median_filter(col, filter_size):
#            col2 = []
#            for i, r in enumerate(col):
#                ls = col[i:i + filter_size]
#                ls.sort()
#                v = ls[int(len(ls) / 2)]
#                col2.append(v)
##                print i, v
#            return col2
#        if median_filters:
#            for f in median_filters:
#                ycol = _median_filter(ycol, f)
#
#        return xcol, ycol
#    def save(self, fname=None, as_zip=True):
#        if not fname:
#            fname = self.auto_name()
#        fname = path(fname)
#    #    fname.abspath().parent.makedirs_p()
##        smeas = dumper.dump(self.data.measurements)
#        df = pd.DataFrame(unbunchify(self.data.measurements))
##        print df
#        buff =StringIO()
#        df.to_csv(buff)
#        smeas=buff.getvalue()
##        print smeas
#        del self.data.measurements
#        s = dumper.dump(self.data, format='yaml')
#        if as_zip:
#            fjson = fname + '.yaml'
#            fzip = fname + '.zip'
#            fcsv=fname + '.csv'
#            with ZipFile(fzip, 'w', compression=ZIP_DEFLATED) as myzip:
#                myzip.writestr(fjson.name, s)
#                myzip.writestr(fcsv.name, smeas)
##                myzip.writestr('schematic.txt', self.data.schematic)
#                print '"%s" was saved' % fzip
#        else:
#            fname.write_text(s)
#    def load(self, fzip):
#        fzip = path(fzip).abspath()
#        with ZipFile(fzip, 'r') as myzip:
##            print myzip.filelist
#            fcsv = filter(lambda x:x.filename.endswith('csv'),myzip.filelist)[0]
#            fyaml = filter(lambda x:x.filename.endswith('yaml'),myzip.filelist)[0]
#            s = myzip.read(fyaml)
#            smeas = myzip.read(fcsv)
#            self.data = unbunchify(dumper.load(s, format='yaml'))
#            df = pd.read_csv(StringIO(smeas), index_col=0)
##            print df
#            self.data['measurements']=df
##            print self.data
#            print '"%s" was loaded' % fzip
#            self.project = self.data['project']
##            self.json=s
    def __getitem__(self, key):
        return self.data[key]


class Schematic(object):
    def __init__(self, project):
        self.project = project

        directory = path(project.directory)
        if (directory.isfile()):
            directory = directory.parent
        self.template_path = directory / SCHEMATIC_TEMPLATE_NAME

    @property
    def template(self):
        return self.template_path.text()

    def replace_variables(self):
        config = self.project.config
        if not config:
            raise ValueError('missing config')
        
        def replace(s, var, value):
            xfrom = ' %s ' % var
#            xto = str(value)
            xto = '%s=%s' % (var, value)
            if len(xfrom) < len(xto):
                xfrom = xfrom.center(len(xto))
            xto = xto.center(len(xfrom))
            return s.replace(xfrom, xto)

        s = self.template
        s = s.replace('\n', '    \n') # add space to line end
            
        for var, value in config.items():
            if isinstance(value, list):
                for i,x in enumerate(value):
                    for var2, value2 in x.items():
                        s=replace(s, '%s_%s'%(var2,i+1), value2)
            s=replace(s, var, value)
#             xfrom = ' %s ' % var
# #            xto = str(value)
#             xto = '%s=%s' % (var, value)
#             if len(xfrom) < len(xto):
#                 xfrom = xfrom.center(len(xto))
#             xto = xto.center(len(xfrom))
# #             if xfrom not in s:
# #                 raise ValueError('"%s" not found in schematic! \n config:%s' %(xfrom, config))
#     #        print '"%s" -> "%s"'%(xfrom,xto)
#             s = s.replace(xfrom, xto)
        return s

    @property
    def text(self):
        return self.replace_variables()


class PlotType(object):

    def __init__(self, project, name='time_plot'):
        self.name = name
        self.project = project
        self.module = self.project.submodule('plot')
        self.func = getattr(self.module, name)

    def display(self, zipfilename='', block=True):
        fig = plt.figure()
        self.create(fig, zipfilename)
        if block:
            plt.show()
        else:
            p = EasyProcess([sys.executable,
                             '-m', 'elme.start.plot',
                             self.project.name,
                             '--plot', self.name,
                             '--zipfilename', zipfilename
                             ])
            p.start()

#            print p
#        if os.fork():pr
#            # Parent
#            plt.show()
#            sys.exit()
#        else:
#            # Child
#            os.setsid()
#            x = np.linspace(-10,10,100)
#            plt.plot(x,arctan(x))
#            plt.show()
#                    proc_num = os.fork()
#        if proc_num == 0:
#            #This is the child process,
#            plt.show()
#            sys.exit()
#        #This is the parent process,
#
#            def show(self,zipfilename,plt):
#                import matplotlib.pyplot as plt
#                fig = plt.figure()
#                print 7777
#                self.create(fig, zipfilename)
#                plt.show()
#                print 8888
#        if block:
#            show()
#        else:
#            p=Process(target=show, args=(self,zipfilename,plt))
#            p.start()
    def create(self, fig, zipfilename):
#        dw = wrapcli(zipfilename, self.project.name)
        data = self.project.load(zipfilename)
        self.func(data, fig)

    def embed(self, zipfilename):
        fig = plt.figure()
        self.create(fig, zipfilename)

    @classmethod
    def all(cls, project):
        module = project.submodule('plot')
        names = [x for x in dir(module) if x.endswith('_plot')]
        names.sort()
        return [cls(project, x) for x in names]

    def __str__(self):
        return self.name


# @traced
class Project(object):

    def __init__(self, name):
        self.name = str(name)
        self.directory = PROJECTS_HOME / name

    @property
    def config(self):
        x = self.default_config
        return x
#        try:
#        self.config = importlib.import_module(
#            'elme.%s.start.config' % name).config
#        except AttributeError:
#            self.config=None

    def __str__(self):
        return self.name

    @property
    def schematic(self):
        return Schematic(self)

    @memoized
    def plot(self, plot_name='time_plot'):
        ls = filter(lambda x: x.name == plot_name, self.allplots())
        if len(ls):
            return ls[0]

    @memoized
    def allplots(self):
        return PlotType.all(self)

    @classmethod
    @memoized
    def all(cls):
        ls = [x.name for x in PROJECTS_HOME.dirs()]
        ls.sort()
        return [cls(x) for x in ls]

    @classmethod
    @memoized
    def find(cls, name):
        ls = filter(lambda x: x.name == name, cls.all())
        if len(ls):
            return ls[0]

    def allmeasurements(self):
        d = self.result_dir
        ls = sorted(d.files(), key=lambda r: r.ctime)
        return ls
#        return CDataWrapper.files(self.name)

    @property
    def default_config_path(self):
        return self.directory / DEFAULT_CONFIG_JSON

    @property
    def default_config(self):
        try:
            s = self.default_config_path.text()
        except IOError:
            return None
        data = dumper.load(s, format=self.default_config_path.ext.strip('.'))
        return data

    @property
    def module_name(self):
        return '%s.%s' % (PROJECTS_MODULE, self.name)

    def submodule_name(self, subname):
        return '%s.%s' % (self.module_name, subname)

    def submodule(self, subname):
        try:
            return  importlib.import_module(self.submodule_name(subname))
        except ImportError:
            pass

    def measure(self, zipfilename=''):
        HOME_DIR.mkdir_p()
        measure_func = self.submodule('measure').measure

        now = datetime.datetime.now()
        data = measure_func(self.config)
        data = bunchify(data)
        data.schematic_template = self.schematic.template
        data.schematic = self.schematic.text
        data.config = self.config
        data.project = self.name
        data.time = str(now)

        self.save(data)
#        dw = CDataWrapper(data)

#        dw.save(zipfilename)

    def analyse(self, zipfilename):
        mod=self.submodule('analyse')
        if not mod:
            return
        analyse_func = mod.analyse
        data = self.load(zipfilename)
        result = analyse_func(data)
#        result=bunchify(result)
        return         result

    def analyse_str(self, zipfilename):
        result = self.analyse(zipfilename)
        if hasattr(result, 'to_string'):
            s = result.to_string(float_format=lambda x: '%g' % x)
        else:
#        pprint(unbunchify(result))
#        result=[ufloat((1,0.1)),'xxx']
#        print result, type(result['Vnull'])
            s = pp_str(result)  # dump(result,format = 'json')

        return         s

    @property
    def result_dir(self):
        d = HOME_DIR / self.name
        if not d.exists():
            d.mkdir_p()
        return d

    def load(self, fzip):
        fzip = path(fzip).abspath()
        with ZipFile(fzip, 'r') as myzip:
#            print myzip.filelist
            fcsv = filter(
                lambda x: x.filename.endswith('csv'), myzip.filelist)[0]
            fyaml = filter(
                lambda x: x.filename.endswith('yaml'), myzip.filelist)[0]
            s = myzip.read(fyaml)
            smeas = myzip.read(fcsv)
            data = unbunchify(dumper.load(s, format='yaml'))
            df = pd.read_csv(StringIO(smeas), index_col=0)
#            print df
#            print self.data
            print '"%s" was loaded' % fzip
#            self.project = self.data['project']
#            self.json=s
            data = bunchify(data)
#            print data
            data['measurements'] = df
#            print data
            return data

    def save(self, data, fname=None):
        if not fname:
            fname = self.auto_name()
        fname = path(fname)
    #    fname.abspath().parent.makedirs_p()
#        smeas = dumper.dump(self.data.measurements)
        df = pd.DataFrame(unbunchify(data.measurements))
#        print df
        buff = StringIO()
        df.to_csv(buff)
        smeas = buff.getvalue()
#        print smeas
        del data.measurements
        s = dumper.dump(data, format='yaml')

        fjson = fname + '.yaml'
        fzip = fname + '.zip'
        fcsv = fname + '.csv'
        with ZipFile(fzip, 'w', compression=ZIP_DEFLATED) as myzip:
            myzip.writestr(fjson.name, s)
            myzip.writestr(fcsv.name, smeas)
#                myzip.writestr('schematic.txt', self.data.schematic)
            print '"%s" was saved' % fzip

    def auto_name(self):
        name = '%s_%s' % (self.name, format_time())
    #    name = name.replace(" ", '_')
#        self.result_dir.makedirs_p()
        return self.result_dir / name
