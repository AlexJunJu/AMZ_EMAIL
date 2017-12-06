#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#向网页渲染
from flask import Flask, request, render_template
from view import ViewClass

app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
	#view = ViewClass()
	DailyInfoList = ViewClass.daily_info_list()
	return render_template('display.html',DailyInfoList=DailyInfoList)

@app.route('/business_report', methods=['GET'])
def business_report():
	#view = ViewClass()
	BusinessReportList = ViewClass.business_report()
	return render_template('business_report.html',BusinessReportList=BusinessReportList)


if __name__ == '__main__':
	app.run()
