#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import AmzSellerOrder  
from email.mime.text import MIMEText
from email.mime.multipart  import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
import time
import random

def get_buyer_email_by_payments_last_day():
	#获取相对本地时间慢1天的下订单的客户的Email
	return AmzSellerOrder.get_buyer_email_by_payments_last_day()

def send_email_of_order_info_subject(Buyer_Order):

	#美国个人站客服账号信息
	from_adress_usye = 'yezidan@gmail.com'
	password_usye = ''


	#北美企业站客服账号信息
	from_adress_us = 'amazonus@aceec.cn'
	#首次登录qq企业在邮箱后的更改之后的密码
	password_us = 'AmzUsAceec1122'
	#qq企业邮箱绑定微信之后需要使用客户端专用密码来登录
	authenication_pwd_us = 'vbG7Enny2SfkSFy4'

	#欧洲企业站客服账号信息,是不带Z的Amaoneu
	from_adress_eu = 'amaoneu@aceec.cn'
	#首次登录qq企业在邮箱后的更改之后的密码
	password_eu = 'Aceec1122'


	#欧洲企业站客服账号信息,是带Z的Amazon
	from_adress_eu_z = 'amazoneu@aceec.cn'
	#首次登录qq企业在邮箱后的更改之后的密码
	password_eu_z = 'AmzEuAceec1122'
	#qq企业邮箱绑定微信之后需要使用客户端专用密码来登录
	authenication_pwd_eu_z = 'xgXrnHTpXtB8PYDD'


	#邮件正文英文内容
	text_content_E = '''
Dear Customer：

Thanks for your recent purchase. I hope you're satisfied with my products and services. 

Don't hesitate to contact me if you have any questions. I will try my best to assist you. 

Thank you again. I am looking forward to serving you again in the future. 

Yours sincerely.
	 '''


	#邮件正文德文内容
	text_content_D =  '''
Liebe Kundin：

vielen Dank für Ihren Einkauf. Wir hoffen, dass Sie mit unseren Produkten und Service zufrieden sind.
Sollten Sie Fragen haben, stehen wir Ihnen gerne zur Verfügung und versuchen unser Bestes, um Ihnen zu helfen.
Wir freuen uns bereits jetzt auf Ihren nächsten Einkauf!

Mit freundlichen Grüßen,
ring love.
	'''

	Asin_List =['B06XG98V1M','B073P9H5XF','B071SM7LTR'\
				'B01LXMBZ0N','B01M4RVJDD','B01N9J8HGQ','B01MZ0C8R0','B01M7UKMR3','B01MRY3M6V','B01N4EID5B','B01MXYW4UK',\
				'B0722K8PMQ','B07116SJCZ','B071KRM6B6','B0722KDD1C','B071V8WD6G','B0718ZVCKJ','B072FHJ5G6','B072FHJNHP',\
				'B071F9JR7T','B071KXFSY7','B071DR1255','B06Y2F56SW','B01M0F5JSW','B076JDWS8F','B0742CJ4VR','B074SNBPGM',\
				'B074CQY1DT','B074PPPS7F','B0742JJMKD','B0742JPR1S']


	English_oriented_stations = ['Amazon.com','Amazon.ca','Amazon.co.uk','Amazon.fr','Amazon.it','Amazon.es']
	German_oriented_stations  = ['Amazon.de']
	North_American_stations   = ['Amazon.com','Amazon.ca']
	Europe_stations = ['Amazon.de','Amazon.co.uk','Amazon.fr','Amazon.it','Amazon.es']


	# from ipdb import set_trace
	# set_trace()

	for buyerOrder in Buyer_Order:
		#构造邮件
		#利用MIMEMultipart构造带附件的邮件
		msg = MIMEMultipart()
		msg['Subject'] = Header('Order Information','utf-8').encode()

		if buyerOrder.name == 'Yerongzhen' and buyerOrder.sales_channel == 'Amazon.com':
			#msg['From'],msg['To'],msg['Subject']用于显示邮件标题信息
			msg['From'] = 'yezidan@gmail.com'
			msg.attach(MIMEText(text_content_E,'plain','utf-8'))

		if buyerOrder.name == 'KingLove' \
			and buyerOrder.sales_channel in English_oriented_stations:
			msg['From'] = 'amazonus@aceec.cn'
			msg.attach(MIMEText(text_content_E,'plain','utf-8'))

		if buyerOrder.name == 'KingLove' \
			and buyerOrder.sales_channel in German_oriented_stations:
			msg['From'] ='amaoneu@aceec.cn'
			msg.attach(MIMEText(text_content_D,'plain','utf-8'))

		#将有附件的asin的附件添加到邮件里
		if buyerOrder.asin in (Asin_List) :
				
			if buyerOrder.sales_channel in English_oriented_stations:
				with open('f:/instruction/'+buyerOrder.asin+'-E.jpg','rb') as f:
					mime = MIMEBase('image','jpg',filename =buyerOrder.asin+'-E.jpg' )
					#添加头部必要信息
					mime.add_header('Content-Disposition','attachment',filename =buyerOrder.asin+'-E.jpg')
					mime.add_header('Content-ID','0')
					mime.add_header('X-Attachment_Id','0')
					mime.set_payload(f.read())
					f.close()
					#采用Base64编码
					encoders.encode_base64(mime)
					#将附件添加到MIMEMultipart
					msg.attach(mime)

			# from ipdb import set_trace
			# set_trace()
			if buyerOrder.sales_channel in German_oriented_stations:
				# filename0 = buyerOrder.asin+'-D.jpg'
				# print(type(filename0))
				# print(buyerOrder.asin,buyerOrder.amazon_order_id)
				# print('f:/instruction/'+buyerOrder.asin+'-D.jpg')
				# print(type('f:/instruction/'+buyerOrder.asin+'-D.jpg'))
				with open('f:/instruction/'+buyerOrder.asin+'-D.jpg','rb') as f:
					mime = MIMEBase('image','jpg',filename =buyerOrder.asin+'-D.jpg' )
					#添加头部必要信息
					mime.add_header('Content-Disposition','attachment',filename =buyerOrder.asin+'-D.jpg')
					mime.add_header('Content-ID','0')
					mime.add_header('X-Attachment_Id','0')
					mime.set_payload(f.read())
					f.close()
					#采用Base64编码
					encoders.encode_base64(mime)
					#将附件添加到MIMEMultipart
					msg.attach(mime)

					# mime.add_header('Content-ID','0')
					# mime.add_header('X-Attachment_Id','0')
					# mime.set_payload(f.read())
					# #采用Base64编码
					# encoders.encode_base64(mime)
					# #将附件添加到MIMEMultipart
					# msg.attach(mime)
		if buyerOrder.name == 'Yerongzhen' and buyerOrder.sales_channel == 'Amazon.com':
			pass
			#登录邮件服务器
			# mail_server = smtplib.SMTP("smtp.gmail.com", 587)
			# mail_server.set_debuglevel(1)
			# mail_server.starttls()
			# mail_server.login(from_adress_usye, password_usye)
			# #发送邮件
			# mail_server.sendmail('yezidan@gmail.com',
			# 					 buyerOrder.buyer_email, 
			# 					  msg.as_string(0)
			# 					)
		if buyerOrder.name == 'KingLove' :
			mail_server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)



			#北美站（美国企业站跟加拿大站）采用QQ企业邮箱
			if buyerOrder.sales_channel in North_American_stations:
				try:
					mail_server.login(from_adress_us, authenication_pwd_us)
				except smtplib.SMTPAuthenticationError as Authentication_Error:
					print('北美站客服邮箱客戶端专用密码失效')
					raise Authentication_Error
					os._exit(0)
				
				#发送邮件
				#北美站的客服邮箱是：amazonus@aceec.cn
				mail_server.sendmail(from_adress_us,
									 buyerOrder.buyer_email, 
									 msg.as_string()
									)
				#仅作为后台观察检测使用
				print(buyerOrder.asin,buyerOrder.amazon_order_id,buyerOrder.sales_channel,buyerOrder.payments_date)



			#欧洲站同样采用QQ企业邮箱
			if  buyerOrder.sales_channel in Europe_stations:
				try:
					mail_server.login(from_adress_eu, password_eu)
				except Esmtplib.SMTPAuthenticationError as Authentication_Error:
					print('欧洲站客服邮箱客戶端专用密码失效')
					raise Authentication_Error
					os._exit(0)
					raise
				#发送邮件
				#欧洲站的客服邮箱是：amazoneu@aceec.cn
				mail_server.sendmail(from_adress_eu,
									 buyerOrder.buyer_email, 
									 msg.as_string()
									)
				#仅作为后台观察检测使用
				print(buyerOrder.asin,buyerOrder.amazon_order_id,buyerOrder.sales_channel,buyerOrder.payments_date)
			

			mail_server.close()
			time.sleep(random.randint(25,35))

	print('byebye')





#if __name__ == '__main__':
#只有把当前.py文件作为脚本执行时，才会执行if __name__ == '__main__'：函数下的程序语句
#import语句是不会执行if __name__ == '__main__'：函数下的程序语句的
if __name__ == '__main__':
	try:
		Buyer_Order = get_buyer_email_by_payments_last_day()
	except Exception as e:
		print('databases connection error!')
	finally:
		send_email_of_order_info_subject(Buyer_Order)
		os._exit(0)






