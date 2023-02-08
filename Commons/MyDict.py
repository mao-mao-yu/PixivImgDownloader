from Commons import *


class MyDict(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if type(value) == dict:
                value = MyDict(**value)
            self[key] = value

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __iter__(self):
        self.iter_index = 0
        self.keys = list(self.__dict__.keys())
        return self

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __next__(self):
        while self.iter_index < len(self.keys):
            if self.keys[self.iter_index] != 'iter_index':
                result = {self.keys[self.iter_index]: self.__dict__[self.keys[self.iter_index]]}
                self.iter_index += 1
                return result
            self.iter_index += 1
        raise StopIteration

    def __getattr__(self, key):
        return getattr(self.__dict__, key)

    def __contains__(self, item):
        return item in self.__dict__

    def __repr__(self):
        return self.__dict__.__repr__()

