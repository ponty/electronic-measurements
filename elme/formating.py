from elme.util import r_round
from uncertainties import nominal_value
from util import none

OMEGA = u'\u03A9'


def round_value(x):
    if none(x):
        return None

#    x = float(nominal_value(x))

    prefix = ''
    if x == 0:
        pass
    elif abs(x) >= 1e9:
        x = x / 1e9
        prefix = 'G'
    elif abs(x) >= 1e6:
        x = x / 1e6
        prefix = 'M'
    elif abs(x) >= 1e3:
        x = x / 1e3
        prefix = 'k'
    elif abs(x) < 1e-9:
        x = x / 1e-12
        prefix = 'p'
    elif abs(x) < 1e-6:
        x = x / 1e-9
        prefix = 'n'
    elif abs(x) < 1e-3:
        x = x / 1e-6
        prefix = 'u'
    elif abs(x) < 1:
        x = x / 1e-3
        prefix = 'm'
    return (x, prefix)


def format_value2(x, prefix, postfix):
    fx = nominal_value(x)
    if fx == int(fx):
        return (u'%0.0f %s%s') % (fx, prefix, postfix)
    else:
        return (u'%0.2f %s%s') % (fx, prefix, postfix)


def format_value(x, postfix):
    (x, prefix) = round_value(x)
    return format_value2(x, prefix, postfix)


def format_ohm(x):
    return format_value(x, OMEGA)


def format_farad(x):
    return format_value(x, 'F')


def format_watt(x):
    return format_value(x, 'W')


def format_charge(x):
    return format_value(x, 'Ah')


def format_ohmE12(x):
    x=r_round(x, rounding='E-12')
    (x, prefix) = round_value(x)
    postfix = OMEGA
    if x >= 10:
        format_str = '%0.0f %s%s'
    elif x >= 1:
        format_str = '%0.1f %s%s'
    else:
        format_str = '%0.2f %s%s'
    return format_str % (x, prefix, postfix)


def format_amper(x):
    return format_value(x, 'A')


def format_volt(x):
    return format_value(x, 'V')


def format_time(x):
    return format_value(x, 's')


def format_percent(x):
    if none(x):
        return ''
    return '%0.1f %%' % (100 * x)


def format_int(x):
    if none(x):
        return ''
    return str(int(x))


def format_beta(x):
    if none(x):
        return ''
    if x > 1:
        return format_int(x)
    else:
        return '%0.1f' % (x)


def format_ufloat(x, format_func):
    if none(x):
        return ''

    if nominal_value(x):
        perc = 100 * x.std_dev() / x.nominal_value
    else:
        perc = 0
    s = u'%10s  \u00B1 %0.1f %% \u00B1 %10s' % (format_func(x.nominal_value),
                                                perc,
                                                format_func(x.std_dev())
                                                )
    return s


def format_uvalue(x, postfix):
    return format_ufloat(x, lambda v: format_value(v, postfix))


def format_analog(x):
    if none(x):
        return ''
    return str(int(nominal_value(x)))

# def format_value(value, error):
#    if value:
#        n = int(log10(error))
#    #    print n
#        return int(round(value, -n))
#
# def format_error(error):
#    if error:
#        n = int(log10(error))
#    #    print n
#        x = (round(error, -n))
#        if x >= 1:
#            x = int(x)
#        return x
