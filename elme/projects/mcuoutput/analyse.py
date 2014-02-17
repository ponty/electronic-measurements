from __future__ import division
from elme.analyse import filter_measurements
from elme.util import an2v


def extend(data):
    m = filter_measurements(
        data.measurements,
        ['Dout', 'pwm_value'],
        ['Aout', 'Aamp']
    )

    R = data.config.R
    vcc = data.vcc

    m['Vout'] = an2v(m.Aout, vcc)
    m['Vamp'] = an2v(m.Aamp, vcc)
    m['I'] = (m.Vout - m.Vamp) / R
    m['Iabs'] = abs(m.I)

    data.measurements = m
