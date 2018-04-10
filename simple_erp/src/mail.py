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

# customer email info of personal state of us
_FROM_ADRESS_YE = 'yezidan@gmail.com'
_PASSWORD_YE = ''

_FROM_BACKUP_ADRESS_YE =  '2016wujunju@gmail.com'
_BACKUP_PASSWORD_YE = 'googlewu4jun7ju8'

#customer QQXMAIL info of north american state
_FROM_ADRESS_US = 'amazonus@aceec.cn'
_PASSWORD_US = 'AmzUsAceec1122'
#QQXMAIL Authorised code afer binding WeChat account 
_AUTHEN_CODE_US = 'vbG7Enny2SfkSFy4'

#customer QQXMAIL info of europe state,without Z,that is,Amaoneu
_FROM_ADRESS_EU = 'amaoneu@aceec.cn'
_PASSWORD_EU = 'Aceec1122'
_AUTHEN_CODE_EU = 'QamxCbDoeVc5c56i'

#customer QQXMAIL info of europe state,with Z,that is,Amazoneu
_FROM_ADRESS_EU_Z = 'amazoneu@aceec.cn'
_PASSWORD_EU_Z = 'AmzEuAceec1122'
#QQXMAIL Authorised code afer binding WeChat account 
_AUTHEN_CODE_EU_Z = 'xgXrnHTpXtB8PYDD'

_QQ_SMTP_SEVER = "smtp.exmail.qq.com"
_QQ_SMTP_PORT = 465

_ENGLISH_ORIENTED_STATES = ['Amazon.com','Amazon.ca','Amazon.co.uk','Amazon.fr','Amazon.it','Amazon.es']
_GERMAN_ORIENTED_STATES  = ['Amazon.de']
_JAPANESE_ORIENTED_STATES = ['Amazon.co.jp']

_NORTH_AMERICAN_STATES   = ['Amazon.com','Amazon.ca']
_EUROPE_STATES = ['Amazon.de','Amazon.co.uk','Amazon.fr','Amazon.it','Amazon.es']

_SHOP_LIST = [
	#{'SHOP':'Yerongzhen','Yerongzhen':{'Email':'yezidan@gmail.com','PASSWORD':'','AUTHEN_CODE':'','STATION':'Amazon.com'}},
	{'SHOP':'KingLove','KingLove':{'Email':'amazonus@aceec.cn','PASSWORD':'AmzUsAceec1122','AUTHEN_CODE':'vbG7Enny2SfkSFy4','STATION':_NORTH_AMERICAN_STATES}},
	{'SHOP':'KingLove','KingLove':{'Email':'amaoneu@aceec.cn','PASSWORD':'Aceec1122','AUTHEN_CODE':'QamxCbDoeVc5c56i','STATION':_EUROPE_STATES}},

]

#content of email in English
_TEXT_CONTENT_E = '''
Dear Customer：

Thanks for your recent purchase. 

I hope you're satisfied with my products and services. 

Don't hesitate to contact me if you have any questions, I will try my best to serve you. 

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
Ring Love.
	'''

_ASIN_WITH_ATTACHEMT_LIST =['B078GFMYSS','B0797S298M','B079L59SVQ',

							'B06XG98V1M','B073P9H5XF','B071SM7LTR',

							'B01LXMBZ0N','B01M4RVJDD','B01N9J8HGQ','B01MZ0C8R0','B01M7UKMR3','B01MRY3M6V','B01N4EID5B','B01MXYW4UK',
							'B0722K8PMQ','B07116SJCZ','B071KRM6B6','B0722KDD1C','B071V8WD6G','B0718ZVCKJ','B072FHJ5G6','B072FHJNHP',
							'B071F9JR7T','B071KXFSY7','B071DR1255','B06Y2F56SW','B01M0F5JSW','B076JDWS8F','B0742CJ4VR','B074SNBPGM',
							'B074CQY1DT','B074PPPS7F','B0742JJMKD','B0742JPR1S']


def get_buyer_email_by_payments_last_day():
	return AmzSellerOrder.get_buyer_email_by_payments_last_day()

def  construct_email(buyerOrder):

	def _extra_mime(msg,mime):
		mime.add_header('Content-ID','0')
		mime.add_header('X-Attachment_Id','0')
		encoders.encode_base64(mime)
		msg.attach(mime)
		return msg

	# create enail with attachement
	#msg['From'],msg['To'],msg['Subject'] are used to display title of emailif
	msg = MIMEMultipart()
	msg['Subject'] = Header('Order Information','utf-8').encode()
	for email_box in _SHOP_LIST:

		if buyerOrder.name == email_box['SHOP'] and buyerOrder.sales_channel in email_box[email_box['SHOP']]['STATION']:
			msg['From'] = email_box[email_box['SHOP']]['Email']
			if buyerOrder.sales_channel in _ENGLISH_ORIENTED_STATES:
				msg.attach(MIMEText(_TEXT_CONTENT_E,'plain','utf-8'))
				if buyerOrder.asin in _ASIN_WITH_ATTACHEMT_LIST:
					mime = MIMEBase('image','jpg',filename =buyerOrder.asin+'-E.jpg' )
					mime.add_header('Content-Disposition','attachment',filename =buyerOrder.asin+'-E.jpg')
					with open('f:/instruction/'+buyerOrder.asin+'-E.jpg','rb') as f:
						mime.set_payload(f.read())
					return _extra_mime(msg,mime)
				else:
					return msg
			elif buyerOrder.sales_channel in _GERMAN_ORIENTED_STATES:
				msg.attach(MIMEText(_TEXT_CONTENT_D,'plain','utf-8'))
				if buyerOrder.asin in _ASIN_WITH_ATTACHEMT_LIST:
					mime = MIMEBase('image','jpg',filename =buyerOrder.asin+'-D.jpg' )
					mime.add_header('Content-Disposition','attachment',filename =buyerOrder.asin+'-D.jpg')
					with open('f:/instruction/'+buyerOrder.asin+'-D.jpg','rb') as f:
						mime.set_payload(f.read())
					return _extra_mime(msg,mime)
				else:
					return msg
			elif buyerOrder.sales_channel in _JAPANESE_ORIENTED_STATES:
				msg.attach(MIMEText('Temporarily empty','plain','utf-8'))
				return msg
			else:
				msg.attach(MIMEText('Temporarily empty','plain','utf-8'))
				return msg
		else:
			continue


def  login_and_send_email(buyerOrder,msg):

	outbox = ''
	outbox_pwd = ''
	station = ''
	for shop in _SHOP_LIST:
		if buyerOrder.name == shop['SHOP'] and buyerOrder.sales_channel in shop[shop['SHOP']]['STATION']:
			outbox = shop[shop['SHOP']]['Email']
			outbox_pwd = shop[shop['SHOP']]['AUTHEN_CODE']
			station = outbox
			break
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
							 msg.as_string(),
							)
		print(buyerOrder.asin,buyerOrder.amazon_order_id,buyerOrder.sales_channel,buyerOrder.payments_date)
		time.sleep(random.randint(50,60))
	finally:
		mail_server.close()


def mail_sending_system():
	try :
		Buyer_Order = get_buyer_email_by_payments_last_day()
	except:
		print('databases connection error!')
	else:
		if len(Buyer_Order)>0:
			for buyerOrder in Buyer_Order:
				msg = construct_email(buyerOrder)
				msg = login_and_send_email(buyerOrder,msg)
			print("auto sending email done")
		else:
			print("No result!")
	finally:
		pass
		
#if __name__ == '__main__':
#only take the current document .py as script to carry out ,the statements in in the if __name__ == '__main__'：can be carry out
#import statement wouldn't carry out the statements in the if __name__ == '__main__'：
if __name__ == '__main__':
		mail_sending_system()
		os._exit(0)