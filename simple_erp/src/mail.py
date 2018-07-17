#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart  import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders

from model import AmzSellerOrder

#customer QQXMAIL info of europe state,with Z,that is,Amazoneu
_FROM_ADRESS_EU_Z = 'amazoneu@aceec.cn'
_PASSWORD_EU_Z = ''
#QQXMAIL Authorised code afer binding WeChat account 
_AUTHEN_CODE_EU_Z = 'D'

_QQ_SMTP_SEVER = "smtp.exmail.qq.com"
_QQ_SMTP_PORT = 465

_ENGLISH_ORIENTED_STATES = ['Amazon.com','Amazon.ca','Amazon.co.uk','Amazon.fr','Amazon.it','Amazon.es']
_GERMAN_ORIENTED_STATES  = ['Amazon.de']
_JAPANESE_ORIENTED_STATES = ['Amazon.co.jp']

_NORTH_AMERICAN_STATES   = ['Amazon.com','Amazon.ca']
_EUROPE_STATES = ['Amazon.de','Amazon.co.uk','Amazon.fr','Amazon.it','Amazon.es']

_SHOP_LIST = [

	{'SHOP':'KingLove','KingLove':{'Email':'amazonus@aceec.cn','PASSWORD':'','AUTHEN_CODE':'','STATION':_NORTH_AMERICAN_STATES}},
	{'SHOP':'KingLove','KingLove':{'Email':'amaoneu@aceec.cn','PASSWORD':'','AUTHEN_CODE':'','STATION':_EUROPE_STATES}},
	{'SHOP':'GuoDong','GuoDong':{'Email':'amazoneu@guodongtouzi.com','PASSWORD':'','AUTHEN_CODE':'','STATION':_EUROPE_STATES}},

]

#content of email in English
_TEXT_CONTENT_E = '''
Dear Customer：

Thanks for your recent purchase. 

I hope you're satisfied with my products and services. 

Don't hesitate to contact me if you have any questions, I will try my best to serve you. 

By the way, please give us a review of honest and friendly Star if you feel the product is good, we'll appreciate that!

Looking forward to serving you again in the future. 

Yours sincerely.
	 '''

#content of email in German
_TEXT_CONTENT_D =  '''
Liebe Kundin：

vielen Dank für Ihren Einkauf. 

Wir hoffen, dass Sie mit unseren Produkten und Service zufrieden sind.
Sollten Sie Fragen haben, stehen wir Ihnen gerne zur Verfügung und versuchen unser Bestes, um Ihnen zu helfen.

Wir freuen uns bereits jetzt auf Ihren nächsten Einkauf!

Mit freundlichen Grüßen,

King Love.

	'''

_ASIN_WITH_ATTACHEMT_LIST =['B078GFMYSS','B0797S298M','B079L59SVQ',

							'B06XG98V1M','B073P9H5XF','B071SM7LTR',

							'B01LXMBZ0N','B01M4RVJDD','B01N9J8HGQ','B01MZ0C8R0','B01M7UKMR3','B01MRY3M6V','B01N4EID5B','B01MXYW4UK',
							'B0722K8PMQ','B07116SJCZ','B071KRM6B6','B0722KDD1C','B071V8WD6G','B0718ZVCKJ','B072FHJ5G6','B072FHJNHP',
							'B071F9JR7T','B071KXFSY7','B071DR1255','B06Y2F56SW','B01M0F5JSW','B076JDWS8F','B0742CJ4VR','B074SNBPGM',

							'B074CQY1DT','B074PPPS7F','B0742JJMKD','B0742JPR1S','B07BVRGW3L']

							'B074CQY1DT','B074PPPS7F','B0742JJMKD','B0742JPR1S']

def get_buyer_email_by_payments_last_day():
	return AmzSellerOrder.get_buyer_email_by_payments_last_day()

def  construct_email(buyerOrder):

	def _return_dic(outbox,outbox_pwd,msg):
		return {'outbox':outbox,
				'outbox_pwd':outbox_pwd,
				'msg':msg,
		}

	def _extra_mime(msg,mime):
		mime.add_header('Content-ID','0')
		mime.add_header('X-Attachment_Id','0')
		encoders.encode_base64(mime)
		msg.attach(mime)
		return msg

	outbox = None
	outbox_pwd = None
	# create enail with attachement
	#msg['From'],msg['To'],msg['Subject'] are used to display title of emailif
	msg = MIMEMultipart()
	msg['Subject'] = Header('Order Information','utf-8').encode()

	for shop in _SHOP_LIST:

		if buyerOrder.name == shop['SHOP'] and buyerOrder.sales_channel in shop[shop['SHOP']]['STATION']:

			outbox = shop[shop['SHOP']]['Email']
			outbox_pwd = shop[shop['SHOP']]['AUTHEN_CODE']
			station = outbox
			msg['From'] = shop[shop['SHOP']]['Email']

			if buyerOrder.sales_channel in _ENGLISH_ORIENTED_STATES:
				msg.attach(MIMEText(_TEXT_CONTENT_E,'plain','utf-8'))
				if buyerOrder.asin in _ASIN_WITH_ATTACHEMT_LIST:
					mime = MIMEBase('image','jpg',filename =buyerOrder.asin+'-E.jpg' )
					mime.add_header('Content-Disposition','attachment',filename =buyerOrder.asin+'-E.jpg')
					with open('f:/instruction/'+buyerOrder.asin+'-E.jpg','rb') as f:
						mime.set_payload(f.read())
					return _return_dic(outbox,outbox_pwd,_extra_mime(msg,mime))
				else:
					return _return_dic(outbox,outbox_pwd,msg)
			elif buyerOrder.sales_channel in _GERMAN_ORIENTED_STATES:
				msg.attach(MIMEText(_TEXT_CONTENT_D,'plain','utf-8'))
				if buyerOrder.asin in _ASIN_WITH_ATTACHEMT_LIST:
					mime = MIMEBase('image','jpg',filename =buyerOrder.asin+'-D.jpg' )
					mime.add_header('Content-Disposition','attachment',filename =buyerOrder.asin+'-D.jpg')
					with open('f:/instruction/'+buyerOrder.asin+'-D.jpg','rb') as f:
						mime.set_payload(f.read())
					return _return_dic(outbox,outbox_pwd,_extra_mime(msg,mime))
				else:
					return _return_dic(outbox,outbox_pwd,msg)
			elif buyerOrder.sales_channel in _JAPANESE_ORIENTED_STATES:
				pass

		else:
			continue

	return _return_dic(outbox,outbox_pwd,msg)

def  login_and_send_email(buyerOrder,mail_info):

	outbox = mail_info.get('outbox')
	outbox_pwd = mail_info.get('outbox_pwd')
	station = outbox
	msg = mail_info.get('msg').as_string() if mail_info.get('msg') is not None else None

	if (outbox is not None
		and outbox_pwd is not None
		and msg is not None):
		try:
			mail_server = smtplib.SMTP_SSL(_QQ_SMTP_SEVER, _QQ_SMTP_PORT)
			mail_server.login(outbox, outbox_pwd)
		except smtplib.SMTPAuthenticationError as Authentication_Error:
			print('%s 客服邮箱客戶端专用密码失效' % station)
			raise Authentication_Error
		except Exception as ex:
			raise ex
		else:
			mail_server.sendmail(outbox,
								 buyerOrder.buyer_email,
								 #"549149676@qq.com",
								 msg,
								)
			print(buyerOrder.asin,
				  buyerOrder.amazon_order_id,
				  buyerOrder.sales_channel,
				  buyerOrder.payments_date,
				  buyerOrder.name,)
			time.sleep(random.randint(50,60))
		finally:
			mail_server.close()
	else:print('%s %s %s %s temporarily Unable to complete ' % (buyerOrder.asin,
																buyerOrder.amazon_order_id,
																buyerOrder.sales_channel,
																buyerOrder.name,))

def mail_sending_system():
	try :
		Buyer_Order = get_buyer_email_by_payments_last_day()
	except:
		print('databases connection error!')
	else:
		if len(Buyer_Order)>0:
			for buyerOrder in Buyer_Order:
				mail_info = construct_email(buyerOrder)
				msg = login_and_send_email(buyerOrder,mail_info)
			print("auto sending email done")
		else:
			print("No result!")
	finally:
		pass

def email(BuyerOrder):
	for buyerOrder in BuyerOrder:
		mail_info = construct_email(buyerOrder)
		msg = login_and_send_email(buyerOrder,mail_info)

def get_list_group_by_name_station():
	KingLoveUsList = []
	KingLoveEuList = []
	GuoDongEuList = []

	Buyer_Order = get_buyer_email_by_payments_last_day()
	for buyerOrder in Buyer_Order:
		if buyerOrder.name == 'KingLove' and buyerOrder.sales_channel in _NORTH_AMERICAN_STATES:
			KingLoveUsList.append(buyerOrder)
		elif buyerOrder.name == 'KingLove' and buyerOrder.sales_channel in _EUROPE_STATES:
			KingLoveEuList.append(buyerOrder)
		elif buyerOrder.name == 'GuoDong' and buyerOrder.sales_channel in _EUROPE_STATES:
			GuoDongEuList.append(buyerOrder)
		
	return KingLoveUsList,KingLoveEuList,GuoDongEuList

def multi_process():

	from multiprocessing import  Process
	from multiprocessing import Pool
	from multiprocessing import cpu_count
	
	cpu_count = len(_SHOP_LIST) if len(_SHOP_LIST) < cpu_count()\
								else  cpu_count()
	pool = Pool(cpu_count)
	group_list = get_list_group_by_name_station()
	for group in group_list:
		pool.apply_async(email,args=(group,))
	pool.close()
	pool.join()
	print("emai jobs is done")
	
#if __name__ == '__main__':
#only take the current document .py as script to carry out ,the statements in in the if __name__ == '__main__'：can be carry out
#import statement wouldn't carry out the statements in the if __name__ == '__main__'：
if __name__ == '__main__':
		#mail_sending_system()
		multi_process()
		os._exit(0)



