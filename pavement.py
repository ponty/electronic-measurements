from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages
import logging
sys.path.insert(0, path('.').abspath())
from pyavrutils import support
import paver.doctools
import paver.virtual
import paver.misctasks
from paved import *
from paved.dist import *
from paved.util import *
from paved.docs import *
from paved.pycheck import *
from paved.pkg import *

# get info from setup.py
setup_py = ''.join(
    [x for x in path('setup.py').lines() if 'setuptools' not in x])
exec(setup_py)


options(
    sphinx=Bunch(
        docroot='docs',
        builddir="_build",
    ),
#    pdf=Bunch(
#        builddir='_build',
#        builder='latex',
#    ),
)


options.paved.clean.rmdirs += ['.tox',
                               'dist',
                               'build',
                               ]
options.paved.clean.patterns += ['*.pickle',
                                 '*.doctree',
                                 '*.gz',
                                 'nosetests.xml',
                                 'sloccount.sc',
                                 '*.pdf',
                                 '*.tex',
                                 'generated_*',  # generated files
                                 'distribute_setup.py',
                                 ]

options.paved.dist.manifest.include.remove('distribute_setup.py')
options.paved.dist.manifest.include.remove('paver-minilib.zip')
options.paved.dist.manifest.include.add('requirements.txt')

docroot = path(options.sphinx.docroot)
root = path(__file__).parent.parent.abspath()
examples = support.find_examples(root)


@task
@needs(
#     'sloccount',
    'cog',
    'html',
#     'pdf',
    'nose',
#     'tox',
)
def alltest():
    'all tasks to check'
    pass


@task
def doxy():
    path('docs/_build/html/doxy').makedirs_p()
    sh('doxygen doxy.ini')


@task
def snippet():
    '''generate screenshots from code snippets'''
    f = docroot / 'code_examples.csv'
    sim.snippet_doc(f, docroot, logger=info)


@task
def libsize():
    f = docroot / 'code4size.csv'
    sim.libsize(f, docroot, logger=info)


@task
def build_test():
    csv = docroot / 'generated_build_test.csv'
    support.build2csv(examples, csv, logdir=docroot / '_build' /
                      'html', extra_lib=root, logger=info)


@task
def boards():
    csv = docroot / 'generated_boards.csv'
    support.boards2csv(csv, logger=info)


@task
@needs('manifest', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our MANIFEST.in is generated.
    """
    pass
