from __future__ import division
from decotrace import traced


def movecol(dataframe, name, position=0):
    dataframe.insert(position, name, dataframe.pop(name))

def addcol(dataframe, name, position=0, default_value=None):
    dataframe.insert(position, name, default_value)
    return dataframe[name]


class ColsProxy(object):
    def __init__(self, dataframe):
        self._dataframe = dataframe

    def __getattr__(self, name):
        if name == '_dataframe':
            return object.__getattribute__(self, name)

        if name not in self._dataframe:
            addcol(self._dataframe, name, position=0)
        return self._dataframe[name]

    def __setattr__(self, name, value):
        if name == '_dataframe':
            self.__dict__[name] = value
            return

        self._dataframe[name] = value
