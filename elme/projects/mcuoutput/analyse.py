from __future__ import division
from softusbduino.util import an2v
from elme.analyse import filter_measurements


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
