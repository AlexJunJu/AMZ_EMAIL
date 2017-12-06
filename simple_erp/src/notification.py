#!/usr/bin/env python3
# _*_coding: utf-8 _*_

from view import ViewClass
from model import AmzDailyBusninessReport

def fba_inv_alert_notification():

	Inv_Alert_List=[]
	view = ViewClass()
	Daily_Info_List = view.daily_info_list()

	for daily_info  in Daily_Info_List:

		if isinstance(daily_info.quantity_left_days,int):
			pass
		else:
			daily_info.quantity_left_days = 99999

		if (daily_info.available_qty == 0)\
			or(daily_info.quantity_left_days < 1)\
			or (daily_info.review_date != '~') :
			print(daily_info.available_qty,daily_info.quantity_left_days,daily_info.review_date)
			Inv_Alert_List.append(daily_info)


	return Inv_Alert_List



def business_report_altert_notification():
	
	Buy_Box_Alert_List = []
	Daily_Business_Report_List = AmzDailyBusninessReport.query_latest_buy_box_percentage()


	for daily_business_report in Daily_Business_Report_List:
		
		if daily_business_report.buy_box_percentage !=  '100%' :
			
			Buy_Box_Alert_List.append(daily_business_report)


	return Buy_Box_Alert_List



if __name__ == '__main__':


	import smtplib
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login( '2016wujunju@gmail.com', 'googlewu4jun7ju8' )





	note_message=""




	Inv_Alert_List = fba_inv_alert_notification()
	for daily_info in Inv_Alert_List:

		
		note_message = note_message + 'marketplace_id:'+ str(daily_info.marketplace_id) \
									+ '\t' \
									+ 'asin:' + str(daily_info.asin) \
									+ '\t' \
									+ 'quantity_available:' + str(daily_info.available_qty) \
									+ '\t' \
									+ 'quantity_left_days:' + str(daily_info.quantity_left_days) \
									+ '\t' \
									+ 'review_date:' + str(daily_info.review_date) \
									+ '\r\n'
		


	Buy_Box_Alert_List = business_report_altert_notification()
	for business_report in Buy_Box_Alert_List:
		
		note_message = note_message + 'marketplace_id:' + str(business_report.marketplace_id) \
									+ '\t' \
									+ 'asin:' + str(business_report.child_asin) \
									+ '\t' \
									+ 'buy_box_percentage:' + str(business_report.buy_box_percentage) \
									+ '\t' \
									+ 'report_date:' + str(business_report.report_date) \
									+ '\r\n'




	msg = "\r\n".join([
						"From: user_me@gmail.com",
						"To: user_you@gmail.com",
						"Notification  Test",
						
						note_message
						])
	# Send text message through SMS gateway of destination number
	server.sendmail('2016wujunju@gmail.com', 
					'549149676@qq.com',     
					msg)
	server.close()