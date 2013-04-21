from nose.tools import eq_
from elme.projects.swing.analyse import longest_good_interval


def test():
    eq_(longest_good_interval([5, 0, 1, 0, 5, 5], 2), [1, 3])
    eq_(longest_good_interval([5, 0, 1, 0], 2), [1, 3])
    eq_(longest_good_interval([0, 1, 0, 5, 5], 2), [0, 2])
    eq_(longest_good_interval([5, 5], 2), None)
    eq_(longest_good_interval([], 2), None)
    eq_(longest_good_interval([0, 5, 1, 0, 5, 5], 2), [2, 3])
