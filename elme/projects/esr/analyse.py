from __future__ import division
from elme.analyse import segmented_measurements, averaged_median_arr
from elme.util import an2v, average
from uncertainties import ufloat


# map_calibration_open = [
#    0.979087650701,
#    0.97955488413,
#    0.979231414833,
#    0.973624613683,
#    0.96223130622,
#    0.933586302912,
#    0.872091195434,
# ]
#        {
#            1000:0.979087650701
#            "frequency": 1000.0
#        },
#        {
#            "R": "465.951888806+/-202.779524848",
#            "calibration_open": "0.97955488413+/-0.00871568197823",
#            "frequency": 2154.4759237315525
#        },
#        {
#            "R": "458.543249437+/-196.512160271",
#            "calibration_open": "0.979231414833+/-0.00871568197823",
#            "frequency": 4641.4481318171265
#        },
#        {
#            "R": "359.000119795+/-121.844405892",
#            "calibration_open": "0.973624613683+/-0.00871568197823",
#            "frequency": 10000.0
#        },
#        {
#            "R": "247.770385088+/-59.4209133828",
#            "calibration_open": "0.96223130622+/-0.00871568197823",
#            "frequency": 21551.724137931036
#        },
#        {
#            "R": "136.7094993+/-19.2171039547",
#            "calibration_open": "0.933586302912+/-0.00871568197823",
#            "frequency": 46403.71229698376
#        },
#        {
#            "R": "66.3076047805+/-5.18086616408",
#            "calibration_open": "0.872091195434+/-0.00871568197823",
#            "frequency": 100000.0
#        }


def avgAV(df, vcc):
    a = averaged_median_arr(df.Ain)
    Ain = ufloat((a, 1))
    Vin = an2v(Ain, vcc)
    return Ain, Vin


def calculate_ohm(data, Vnull, Ain):
    vcc = data.vcc
#    print 'calibration', calibration
    Vin = an2v(Ain, vcc)
#    Ain, Vin = maxi(ls, vcc)

    R1 = data.config.R1
    R2 = data.config.R2

    Ramp1 = data.config.Ramp1
    Ramp2 = data.config.Ramp2

#    def perc1(x):
#        return ufloat((x, x * 0.01))
    Rout = 24

#    R1 = perc1(R1) + ufloat((Rout, Rout * 0.1))
#    R2 = perc1(R2)
    R1 = R1 + Rout

#    Ramp1 = perc1(Ramp1)
#    Ramp2 = perc1(Ramp2)

    A = Ramp2 / Ramp1

    Vgen = R2 / (R2 + R1) * vcc
    Rgen = R1 * R2 / (R1 + R2)

#    print R2, Vgen, Rgen, vcc, R1
    Vampout = Vin
    Vampout_pp = 2 * (Vampout - Vnull)
    Vampin_pp = Vampout_pp / A
    divider = (Vampin_pp / Vgen)

    def calc_Rx(cal):
        return  Rgen / (1 - divider / cal) - Rgen
    Rx_raw = calc_Rx(1)

    calibration_open = Vampin_pp / Vgen

#    calibration = 0.93
#    Rx_cal = calc_Rx(calibration)

#    def calibration_x(x):
#        return divider / (1 - (Rgen / (x + Rgen)))
#    print 555, calibration_x(1.8)

    Rx = Rx_raw
#    print 'Rx_raw,Rx_cal', Rx_raw, Rx_cal
#    if Rx > 30:
#        Rx = None
    return Rx, calibration_open


def analyse1(data, calibration=0.94):
    vcc = data.vcc

    grouped = segmented_measurements(
        data.measurements[['frequency', 'dc', 'Ain']], ['frequency', 'dc'])
#    print (0.0, 0) in dict(grouped).keys()
    for (f, dc), group in grouped:
        if f == 0:
#            print dc
#            print group
            if dc == 0:
                _, V0 = Ain, Vin = avgAV(group, vcc)
            else:
                _, V255 = Ain, Vin = avgAV(group, vcc)

    Vnull = average([V0, V255])
#    d = SortedDict(d)[2:]
#    dRx = SortedDict()
#    for (f, dc), ls in d.items():
#        if not f:
#            continue
#        R, calibration_open = calculate_ohm(data, Vnull, ls)
#        dRx[f] = dict(frequency=f,
#                      R=R,
#                      )

    def maxi(ls):
        # drop 1% on top
#        ls = list(df)
#        ls.sort()
#        drop = int(len(ls) * 0.05)
#        i = len(ls) - drop - 1
#        a = ls[i]
        a = ls.quantile(q=0.99)
    #    a = averaged_median()
        Ain = ufloat((a, 1))
    #    Vin = an2v(Ain, vcc)
        return Ain
    filtered = grouped.agg(maxi)
    del filtered['dc']
    filtered = filtered.drop([0, 1])  # rows
#    print 44,filtered
    dRx, calibration_open = calculate_ohm(data, Vnull, filtered['Ain'])
#    dRx=
#    print 44,filtered
    filtered['Rx'] = dRx
#    print 44,filtered
#    filtered['calibration_open']=calibration_open
#    print 55,filtered
#    print filtered
#    print dict(x=filtered)
#        print dict(row)
    return filtered
#    return dict(
#        V0=V0,
#        V255=V255,
#        Vnull=Vnull,
#        #        Vx=Vampout,
#        Rx=filtered,
##        Rx_cal=Rx_cal,
##        calibration_open=calibration_open,
#    )
analyse = analyse1
# def analyse(data, calibration=0.94):
#    filtered=analyse1(data, calibration=calibration)
#    dicR = [dict(row) for row_index, row in filtered.iterrows()]
#    return dicR
