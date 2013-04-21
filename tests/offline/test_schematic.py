from nose.tools import eq_
from path import path
from elme.project import Project


def test_templates():
    fname = path(__file__).parent / 'generated_schematic_templates.txt'
    f = open(fname, 'w')
    for p in Project.all():
        print p.name
        f.write('\n*******************************  ')
        f.write(p.name)
        f.write('  *******************************\n')
        f.write(p.schematic.template)
    f.close()


def test_schematics():
    fname = path(__file__).parent / 'generated_schematics.txt'
    f = open(fname, 'w')
    for p in Project.all():
        print p.name
        f.write('\n*******************************  ')
        f.write(p.name)
        f.write('  *******************************\n')
        try:
            f.write(p.schematic.text)
        except ValueError as e:
            f.write(str(e))
    f.close()
