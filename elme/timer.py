from __future__ import division

import datetime
import time


# class Timer(object):
#    firstcall = True
#
#    def __init__(self):
#        pass
#
#    def measure(self):
#        self.t = time.time()
#        if self.firstcall:
#            self.tstart = self.t
#            self.firstcall = False
#
#    def startdatetime(self):
#        return datetime.datetime.fromtimestamp(self.tstart)
#
#    def relativ(self):
#        return self.t - self.tstart


class TimeOutError(Exception):
    pass


class Stopwatch(object):
    _tlast_log = 0
    
    def __init__(self, count=None):
        self._count=count
        self.start()
        
    def start(self):
        self._tlast = self._tstart = time.time()
    restart = start

    def read(self):
        self._tlast = time.time()
        return self._tlast - self._tstart

    @property
    def last(self):
        return self._tlast - self._tstart

    def check_timeout(self, timeout):
        if self.read() > timeout:
            tfrom = datetime.datetime.fromtimestamp(self._tstart)
            tto = datetime.datetime.fromtimestamp(self._tlast)
            raise TimeOutError("Timeout! %s sec (from:%s to:%s)" % (timeout,
                                                                    tfrom,
                                                                    tto,
                                                                    ))
            
    def next(self, measurements):
        t = time.time()
        if t-self._tlast_log > 1:
            self._tlast_log=t
            if self._count is not None:
                print  100*len(measurements) / self._count, '%'
            else:
                print  len(measurements)
                
