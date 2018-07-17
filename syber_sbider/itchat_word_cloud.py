#!usr/bin/evn python3
##-*- coding:utf-8 -*-
import itchat
import re
import os

from scipy.misc import imread
from math import sqrt
from PIL import Image
#from wordcloud import WordCloud

#from word_cloud import process_chinese_with_para

_BASE_PARH = 'F:/program/syber_sbider/profile_photos'

def login_wechat():
	itchat.login()

def auto_login():
	itchat.auto_login()

def auto_login_long():
	if itchat.auto_login(hotReload=True):
		return True


def get_get_all_friends():
	friends = itchat.get_friends(update=True)[0:]
	return friends

def send_msg_to_someone():
	users = itchat.search_friends(name = u'郭耀光')
	print(users)
	user_name = users[0]['UserName']
	itchat.send(u"Hello",toUserName=user_name)



def get_all_signature():
	friends = get_get_all_friends()
	str =""
	for f in friends:
		signature= f['Signature'].replace("span","").replace("class","").replace("emoji","")
		rep = re.compile('<.*>')
		signature = rep.sub("",signature)
		print(signature)
		str = str + signature
	return str

def get_all_profile_photos():
	RE_EXPR = "[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]"
	friends = get_get_all_friends()
	i = 0
	for friend in friends:
		profile_photo = itchat.get_head_img(userName=friend['UserName'])
		path = _BASE_PARH + '/'+ str(i) + ".jpg" 
		try:
			with open (path, 'wb') as f:
				f.write(profile_photo)
		except Exception as e:
			raise
		else:
			i=i+1
	

def generate_split_joint_img():
	_path = 'F:/program/syber_sbider/split_joint_img'

	def _get_count_photos():
		photo_list = []
		for photo in os.listdir(_BASE_PARH):
			photo_list.append(photo)

		return len(photo_list)

	photo_nums = _get_count_photos()
	split_joint_row = int(sqrt(photo_nums))
	NewImage = Image.new('RGB',(128*split_joint_row,128*split_joint_row))
	x = y = 0
	for i in range(0,photo_nums+1):
		try:	
			img = Image.open(_BASE_PARH + '/'+ str(i) + ".jpg")
		except Exception as e:
			print("第%d行,%d列文件读取失败！IOError:" % (y,x))
			x -= 1
		else:
			img = img.resize((128,128),Image.ANTIALIAS)
			NewImage.paste(img,(x * 128 , y * 128))
			x+=1
			if x == split_joint_row:
				x = 0
				y += 1
			if (x+split_joint_row*y) == split_joint_row*split_joint_row:
				break
	print('Hello')
	NewImage.save(_path+"/final.jpg")

def word_cloud_setting():
	#must instantiate before call function generate(text)
	word_cloud = WordCloud(
		mask = wordcloud_shape,
		background_color = 'white',
		max_words =2000,
		font_path=font,
		min_font_size = 10
		)
	#generate function generates text cloud according the text
	word_cloud_img = word_cloud.generate(text)

	import matplotlib.pyplot as pyplot
	pyplot.imshow(word_cloud_img, interpolation='bilinear')
	pyplot.axis("off")
	pyplot.show()
	word_cloud.to_file("wordcloud.png")


def generat_word_cloud(wordcloud_shape,font,text):

	wordcloud_shape = imread(r'C:/Users/ACEEC/Downloads/HG.png') 
	# background_color  =  ''
	# sacale = ''
	# Shielding_words = ''
	font = r'C:/Users/ACEEC/Downloads/font163/simheittf.ttf'

	str = get_all_signature()
	text = process_chinese_with_para(str)
	generat_word_setting(wordcloud_shape,font,text)




if __name__ == '__main__':
	#login_wechat()
	# str = get_all_signature()
	# text = process_chinese_with_para(str)
	# generat_word_cloud(wordcloud_shape,font,text)
	#get_all_profile_photos()
	#generate_split_joint_img()
	auto_login_long()