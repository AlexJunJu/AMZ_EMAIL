# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import os.path
from pprint import pprint
from utils import Singleton, dict2object

#配置文件路径
#os.path.dirname(path)， 返回文件路径（不包括文件名）
#os.path.realpath(__file__)，返回path的真实路径，注意区别于相对路径
#__file__，是指当前脚本的完整路径，包括存放路径与文件名
_CONF_FILE_PATH_ = os.path.dirname(os.path.realpath(__file__)) + '\conf'

#配置文件路径下的默认配置文件
#os.path.join(path1[, path2[, ...]])  ，把目录和文件名合成一个路径
_DEFAULT_CONFIG_FILE_ = os.path.join(_CONF_FILE_PATH_, 'config.json')

#测试
print(_DEFAULT_CONFIG_FILE_)
#关于json方法的说明
#json.dumps(),可以将特定的对象序列化处理 为字符串
#json.loads(),可以将形似dict,list的字符串 反序列化为 dict，list
#json.dump(), 把序列化后的字符串写到一个文件中
#json.load(), 则可以从文件中读取数据，处理成为对应的python数据类型
#json字符串中的字典必须是双引号
#注意json数据类型与python中数据类型转化对照


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
        return cls(_DEFAULT_CONFIG_FILE_)

    @classmethod
    def load(cls, path=None):
        return Configuration(path)

    def print_data(self):
        print(self.data)

# In python, import module will be run automatically, so we need to start it  here.
Configuration.load(_DEFAULT_CONFIG_FILE_)
