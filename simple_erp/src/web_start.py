#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#向网页渲染
from flask import Flask, request, render_template
from view import ViewClass

app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
	view = ViewClass()
	#DailyInfoList = ViewClass.daily_info_list()
	DailyInfoList = view.daily_info_list_new()
	return render_template('display.html',DailyInfoList=DailyInfoList)

@app.route('/business_report', methods=['GET'])
def business_report():
	#view = ViewClass()
	BusinessReportList = ViewClass.business_report()
	return render_template('business_report.html',BusinessReportList=BusinessReportList)


import functools
import collections


def decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        if len(args) == 1:
            arg = args[0]
            if not isinstance(arg, collections.Iterable):
                cls_name = type(arg).__name__
                raise TypeError(f'{cls_name} is not iterable')

            if not arg:
                if 'default' in kwargs:
                    return kwargs['default']
                raise ValueError(f'{fn.__name__}() arg is an empty sequence')

            args = arg

        key_func = kwargs.get('key', None)

        items = sorted(args, key=key_func)

        return items[-1]

    return wrapper


@decorator
def customized_max(*args, key=None):
    """
    max(iterable, *[, default=obj, key=func]) -> value
    max(arg1, arg2, *args, *[, key=func]) -> value

    With a single iterable argument, return its biggest item. The
    default keyword-only argument specifies an object to return if
    the provided iterable is empty.
    With two or more arguments, return the largest argument.
    """
    pass


在以前的开发经历中，你遇到过最大的挑战是什么？有何收获？
答：
挑战：在以前的开发经历中，有遇到过非常多的挑战，这其中最大的挑战应当是对业务的透彻理解
收获：尽量与需求方核对清楚需求，要站在业务发展的角度去思考问题，这样才能写出高可用的、易于扩展的代码，也才能够快速的响应业务扩展以及服务，也更好的帮助同事理解业务以及相应的的业务代码；
      尽可能将功能代码划分成一个个小函数，方便复用的同时也可以防止因重复代码的无限熵增而造成后期扩展维护困难。

if __name__ == '__main__':
	app.run()
