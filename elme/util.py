from _abcoll import Iterable
from abc import ABCMeta
from decotrace import traced
from math import log10, floor
from path import path
from traits.has_traits import cached_property, HasTraits
from traits.trait_types import Float
from traits.traits import Property
import itertools
import tempfile
import time


e12 = (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10.0)


def notnone(x):
    return x is not None


def none(x):
    return x is None


def log_split(x):
    if x <= 0:
        return 0, 0
    lx = log10(x)
    return 10 ** (lx - floor(lx)), 10 ** (floor(lx))


def r_round(R, rounding=None):
    if none(R):
        return None
    if rounding == 'E-12':
        br, ten = log_split(R)
        d = dict([(abs(br - x), x) for x in e12])
        k = min(d.keys())
        R = d[k] * ten
        if R == int(R):
            R = int(R)
    return R


def prop(depends_on=None, **kwargs):
    def func(fget):
        fget.__name__ = '_get_' + fget.__name__
        fget = cached_property(fget)
        x = Property(depends_on=depends_on, fget=fget, force=True, **kwargs)
        return x
    return func


def check_duration(func):
    def wrapper(self, *arg):
        t1 = time.time()
        self.valid = func(self, *arg)
        t2 = time.time()
        dt = t2 - t1
        if 'duration' not in self.traits():
            self.add_trait('duration', Float())
        self.duration = dt

    return wrapper


def link_traits(obj1, obj2, name, alias=None):
    setattr(obj1, name, getattr(obj2, name if none(alias) else alias))
    obj1.sync_trait(name, obj2, alias=alias)


def tmpfile(ext):
    f = tempfile.NamedTemporaryFile(prefix='dot', suffix=ext, delete=0)
    f.close()
    return f.name


class IterableNoString:
    __metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, C):
        if cls is IterableNoString:
            if issubclass(C, basestring):
                return False
        return NotImplemented
IterableNoString.register(Iterable)


def isiterable(usrData):
    """
    Returns True if is the object can be iter'd over
    """
    if isinstance(usrData, IterableNoString):
        return True
    else:
        return False


def print_traits(obj, recursive=False):
    if isiterable(obj):
        for x in obj:
            print_traits(x)

    elif isinstance(obj, HasTraits):
        print
        print '=============================================='
        print type(obj)
        print '=============================================='
        obj.   print_traits()

        d = obj.traits()
        for x in d:
            try:
                print_traits(getattr(obj, x))
            except:
                pass


def schema_replace(templ, conf, variables):
    s = templ
    for xfrom in variables:
        xto = str(conf[xfrom])
        if len(xfrom) < len(xto):
            xfrom = xfrom.rjust(len(xto))
        xto = xto.center(len(xfrom))
#        print '"%s" -> "%s"'%(xfrom,xto)
        s = s.replace(xfrom, xto)
    return s


def fullrange(start, stop):
    return range(start, stop + 1)


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def sleep_and_read(t, p_in):
    t0 = time.time()
    t1 = t0 + t
    while time.time() < t1:
        p_in.read_analog()


def tmpdir(dir=None, suffix=''):
    x = tempfile.mkdtemp(suffix=suffix, prefix='elme_', dir=dir)
    return path(x)
