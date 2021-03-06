from path import path
from setuptools import find_packages
import logging


def read_project_version(py=None, where='.', exclude=['bootstrap', 'pavement', 'doc', 'docs', 'test', 'tests', ]):
    if not py:
        py = path(where) / find_packages(where=where, exclude=exclude)[0]
    py = path(py)
    if py.isdir():
        py = py / '__init__.py'
    __version__ = None
    for line in py.lines():
        if '__version__' in line:
            exec line
            break
    return __version__

# release = read_project_version(path('..').abspath() / 'sphinxcontrib' /
# 'eagle.py')

release = '0.0.0'
project = u'electronic-measurements'
copyright = u'2013, ponty'
author = 'ponty'


# logging.basicConfig(level=logging.DEBUG)

needs_sphinx = '1.0'

extensions = [
    # -*-Extensions: -*-
    #     'sphinx.ext.autodoc',
    #     'sphinxcontrib.programoutput',
    'sphinxcontrib.programscreenshot',
    #     'sphinx.ext.graphviz',
    #     'sphinxcontrib.autorun',
    #'sphinx.ext.autosummary',
    #     'sphinx.ext.intersphinx',
    #      'matplotlib.sphinxext.mathmpl',
    'matplotlib.sphinxext.only_directives',
    'matplotlib.sphinxext.plot_directive',
    #      'matplotlib.sphinxext.ipython_directive',
]

# intersphinx_mapping = {'http://docs.python.org/': None,
#'http://packages.python.org/sphinxcontrib-programoutput/' : None,
#}

source_suffix = '.rst'
master_doc = 'index'


exclude_patterns = ['_build/*']

html_theme = 'default'
html_static_path = []

# intersphinx_mapping = {
#    'ansi': ('http://packages.python.org/sphinxcontrib-ansi', None)}


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')


# latex build settings
latex_documents = [
    ('index', '%s.tex' % project, u'%s Documentation' % project,
     author, 'manual'),
]

# remove blank pages from pdf
# http://groups.google.com/group/sphinx-
# dev/browse_thread/thread/92e19267d095412d/d60dcba483c6b13d
latex_font_size = '10pt,oneside'

latex_elements = dict(
    papersize='a4paper',
)
