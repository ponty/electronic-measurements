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

    def __init__(self):
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
