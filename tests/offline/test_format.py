from nose.tools import eq_
from elme.formating import format_ohmE12
from elme.util import log_split, r_round


def almost_eq(a, b):
    d = abs(a - b)
    assert d < 0.001, (a, b)


def test_log_split():
    eq_(log_split(1), (1, 1))
    eq_(log_split(10), (1, 10))

    almost_eq(log_split(125)[0], 1.25)
    eq_(log_split(125)[1], (100))

    almost_eq(log_split(0.0125)[0], 1.25)
    eq_(log_split(0.0125)[1], (0.01))
    almost_eq(log_split(125000)[0], 1.25)
    eq_(log_split(125000)[1], (100000))
    almost_eq(log_split(12.5)[0], 1.25)
    eq_(log_split(12.5)[1], (10))

#    almost_eq(log_split(0.0046)[0], 4.6)
#    eq_(log_split(0.0046)[1], (0.001))


def test_r_round():
    eq_(r_round(1.0), 1.0)
    eq_(r_round(1.0, rounding='E-12'), 1.0)
    eq_(r_round(1.01, rounding='E-12'), 1.0)
    eq_(r_round(1.19, rounding='E-12'), 1.2)
    eq_(r_round(9.9, rounding='E-12'), 10)
    eq_(r_round(400, rounding='E-12'), 390)
    eq_(r_round(0.0046, rounding='E-12'), 0.0047)


def test_format():
    def ohm(x):
        return x + u'\u03a9'
    eq_(format_ohmE12(1), ohm('1.0 '))
    eq_(format_ohmE12(4700), ohm('4.7 k'))
    eq_(format_ohmE12(1000), ohm('1.0 k'))
