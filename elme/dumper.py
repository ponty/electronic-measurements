from bunch import bunchify, unbunchify
from decotrace import traced
from uncertainties import ufloat
import json as jsondump
import omnijson as jsonload
import uncertainties
import yaml


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



def string_presenter(dumper, data):
    lines = data.splitlines()
    if len(lines) > 1:
        style = '|'
        lines = [x.rstrip() for x in lines]
        data = '\n'.join(lines)
    else:
        style = ''

    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=style)
yaml.add_representer(str, string_presenter, Dumper=Dumper)
yaml.add_representer(unicode, string_presenter, Dumper=Dumper)



def ufloat_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', str(data), style='')
# yaml.add_representer(uncertainties.Variable, ufloat_presenter, Dumper=Dumper)
yaml.add_representer(
    uncertainties.AffineScalarFunc, ufloat_presenter, Dumper=Dumper)


def load(text, format='json'):
    data = None
    if format == 'json':
        data = jsonload.loads(text)
    if format == 'yaml':
        data = yaml.load(text, Loader=Loader)
    assert data, format
    return bunchify(data)


def dump(data, format='json'):
    data = unbunchify(data)
    s = None
    if format == 'json':
        s = jsondump.dumps(data, indent=4)
    if format == 'yaml':
        s = yaml.dump(data, Dumper=Dumper, default_flow_style=False)
    assert s, format
    return s
