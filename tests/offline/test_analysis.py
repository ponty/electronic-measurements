
from nose.tools import eq_
from pandas.core.frame import DataFrame
from elme.analyse import segmented_measurements, filter_measurements


def test_filt():
    df = DataFrame(
        dict(
            a=['aa', 'aa', 'aa', 'aa', 'b', 'b'],
            b=[2, 2, 3, 3, 5, 5],
            c=[1, 2, 3, 4, 5, 6],
            d=[31, 32, 33, 44, 44, 66],
        )
    )
    m = filter_measurements(
        df,
        ['a', 'b'],  # keys
        ['c', 'd']
    )
    print m.to_string()
    eq_(['aa', 'aa', 'b'], list(m.a))
    eq_([2, 3, 5], list(m.b))
# def xsegmented_measurements(data, keys):
#    x=segmented_measurements(DataFrame(data), keys)
#    return x
#
# def test_1key():
#    eq_(
#        [({'b': 2}, [{'a': 1, 'b': 2}])],
#        xsegmented_measurements([dict(a=1, b=2)], ['b'])
#    )
#
#    eq_(
#        [({'b': 2}, [{'a': 1, 'b': 2}, {'a': 2, 'b': 2}]),
#         ({'b': 3}, [{'a': 3, 'b': 3}, {'a': 4, 'b': 3}])], segmented_measurements([
#                                                                                   dict(a=1, b=2),
#                                                                                   dict(a=2, b=2),
#                                                                                   dict(a=3, b=3),
#                                                                                   dict(a=4, b=3),
#                                                                                   ], ['b'])
#    )
#
#
# def test_2keys():
#    eq_(
#        [({'a': 1, 'b': 2}, [{'a': 1, 'b': 2}])],
#        segmented_measurements([dict(a=1, b=2)], ['a', 'b'])
#    )
#
#    eq_(
#        [(
#            {'c': 0, 'b': 2}, [{'a': 1, 'c': 0, 'b': 2}, {'a': 2, 'c': 0, 'b': 2}]),
#       ({'c': 0, 'b': 3}, [{'a': 3, 'c': 0, 'b': 3}]),
#            ({'c': 1, 'b': 3}, [{'a': 4, 'c': 1, 'b': 3}, {'a': 4, 'c': 1, 'b': 3}])], segmented_measurements([
#                                                                                                              dict(a=1, b=2, c=0),
#                                                                                                              dict(a=2, b=2, c=0),
#                                                                                                              dict(a=3, b=3, c=0),
#                                                                                                              dict(a=4, b=3, c=1),
#                                                                                                              dict(a=4, b=3, c=1),
#                                                                                                              ], ['b', 'c'])
#    )
