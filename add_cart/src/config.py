from __future__ import absolute_import
import json
import os.path
from pprint import pprint
from utils import Singleton, dict2object

_CONF_FILE_PATH_ = os.path.dirname(os.path.realpath(__file__)) + '/conf'


class Configuration(object):
    __metaclass__ = Singleton

    def __init__(self, path=None):
        try:
            with open(path, 'r') as handle:
                self.data = json.load(handle)
                self.conf = dict2object(self.data)

        except IOError:
                raise Exception("%s is not found" % path)

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def load(cls, path=None):
        return Configuration(path)

    def print_data(self):
        pprint(self.data)

# In python, import module will be run automatically, so we need to start it
# here.
_DEFAULT_CONFIG_FILE_ = os.path.join(_CONF_FILE_PATH_, 'config.json')
Configuration.load(_DEFAULT_CONFIG_FILE_)
