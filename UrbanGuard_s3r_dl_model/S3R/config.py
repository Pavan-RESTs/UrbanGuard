import numpy as np
import os
import shutil

    
class Config(object):
    def __init__(self, lr):
        self.lr = lr
        try:
            
            terminal_size = shutil.get_terminal_size()
            self.envrows, self.envcols = terminal_size.lines, terminal_size.columns
        except OSError:
            
            self.envrows, self.envcols = 24, 80

    def __str__(self):
        attrs = vars(self)
        attr_lst = sorted(attrs.keys())
        return '\n'.join("- %s: %s" % (item, attrs[item]) for item in attr_lst if item != 'lr')


class Obj(object):
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(v, (list, tuple)):
               setattr(self, k, [Obj(x) if isinstance(x, dict) else x for x in v])
            else:
               setattr(self, k, Obj(v) if isinstance(v, dict) else v)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

