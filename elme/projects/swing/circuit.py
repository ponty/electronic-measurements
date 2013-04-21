from __future__ import division


class Circuit(object):
    def __init__(self,
                 A,
                 Vplus=None,
                 Vminus=None,
                 Vout=None,
                 ):
        self.A = A
        self.Vplus = Vplus
        self.Vminus = Vminus
        self.Vout = Vout

        if len(filter(lambda x: x is None, [Vplus, Vminus, Vout])) != 1:
            raise ValueError('only one parameter can be None!')

        if Vplus is None:
            self.Vplus = Vminus + (Vout - Vminus) / (1 + A)

        if Vminus is None:
            self.Vminus = Vplus - (Vout - Vplus) / A

        if Vout is None:
            self.Vout = Vminus + (1 + A) * (Vplus - Vminus)
