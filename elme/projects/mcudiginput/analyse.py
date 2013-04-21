from __future__ import division
from elme.analyse import filter_measurements
from softusbduino.util import an2v


# @traced


def extend(data):
#    dw = DataWrapper(data)
    data.measurements = filter_measurements(
        data.measurements, ['pwm_value', 'rail'], ['Aout', 'Ain', 'Aamp'])
#    print 111,unbunchify(dw.data)
#    print 222,(dw.data)
    R = data.config.R
    vcc = data.vcc
#    def calc(x):
#            x.Vin = an2v(x.Ain, vcc)
#            x.Vout = an2v(x.Aout, vcc)
#            x.Vamp = an2v(x.Aamp, vcc)
#            x.Vx = x.Vout - x.Vin
#            x.I = (x.Vin - x.Vamp) / R
    data.Vmax = data.vcc
    data.Imax = data.vcc / R
#    ls=[]
#    pwm_current=0
#    for x in dw.data.measurements:
#        # group by pwm_value
#        x.pwm_value==pwm_current:
#            ls.append(x)
#        else:
#            calc(x)
#            ls=[]
#            pwm_current=x.pwm_value
    d = groupped_measurements(data.measurements, ['pwm_value', 'rail'])
    for p in range(256):
        for r in [0, 1]:
            ls = d[p, r]
# ls = [x for x in dw.data.measurements if x.pwm_value == p and x.rail ==
# r]
            if not len(ls):
                continue

            Ain = ls[0].Ain
            Aout = ls[0].Aout
            Aamp = ls[0].Aamp

            Vin = an2v(Ain, vcc)
            Vout = an2v(Aout, vcc)
            Vamp = an2v(Aamp, vcc)
            Vx = Vout - Vin
            I = (Vin - Vamp) / R

            for x in ls:
                x.I = I
                x.Vx = Vx
                x.Vin = Vin
                x.Vout = Vout
                x.Vamp = Vamp
#    print dw.data
#    return data
