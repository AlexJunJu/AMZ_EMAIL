#!/usr/bin/env python3
import os
import time
import random
import requests
#dynamic request
#import

#lib beautifulsoup4 and lxml can quickly  analyze html
from bs4 import BeautifulSoup
from selenium import webdriver

class WebDriver(object):
	"""docstring for WebDriver"""
	def __init__(self):
		self.Browser_Head_Agent = {'User-Agent': 
									'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
	@classmethod	
	def browser_chrome(cls):

		from selenium.webdriver.chrome.options import Options
		
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--proxy-server=http://202.20.16.82:10152')
		web_deriver = webdriver.Chrome(chrome_options=chrome_options)
		return web_deriver

	@classmethod
	def browser_firefox(cls):
		web_deriver = webdriver.Firefox()
		return web_deriver



class dynamic_sbyder():
	def __init__(self):
		#Given url and parameters
		#self.web_url = 'http://unsplash.com'
		self.web_url = 'https://www.zhihu.com/question/23819007'
		self.times = 10
		self.url_paras = {}
		self.folder_path = 'F:\program\syber_sbider\down_load_img'

	def is_folder_Exists(self,folder_path):
		folder_path = folder_path.strip()
		isExists = os.path.exists(folder_path)
		print(isExists)
		return isExists

	def mkdir(self,folder_path):
		isExists  = self.is_folder_Exists(folder_path)
		if not isExists:
			print("Folder is creating……")
			os.makedirs(folder_path)
			print(folder_path, 'Folder created successefully')
		else:
			pass
		os.chdir(self.folder_path)
		return os.getcwd()

	def scroll_down(self,deriver,times):
		for t in range(times):
			print('start to scroll_down',str(t+1))
			deriver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
			print(str(t+1),'scroll_down completed')
			time.sleep(random.randint(3,10))
	
	def get_files(self,folder_path):
		file_names = os.listdir(folder_path)
		return file_names

	def send_requests(self,web_url):
		print("Web Page Get requests Starts:")
		#send the target URL a get request,return a response object
		resp = requests.get(web_url)
		return resp

	def get_all_img_url(self):
		print('start to send requests……')
		web_deriver = WebDriver.browser_chrome()
		web_deriver.get(self.web_url)
		self.scroll_down(deriver= web_deriver,times=self.times)
		all_img = BeautifulSoup(web_deriver.page_source,'lxml').findAll('a',title="Download photo")

		print("img标签的数量是：",len(all_img))
		return all_img

	def get_all_answers(self):
		print('start to send requests……')
		web_deriver = WebDriver.browser_chrome()
		web_deriver.get(self.web_url)
		self.scroll_down(deriver= web_deriver,times=self.times)
		all_answers = BeautifulSoup(web_deriver.page_source,'lxml').find('meta',itemprop="url")
		print(type(all_answers))
		print(all_answers)
		

	def img_name(self,img_url):
		# use silce to idetify the longth of url
		name_start_pose = img_url.index('photos')+len('photos/')
		name_end_pose = img_url.index('download?')-len('/')
		img_name = img_url[name_start_pose:name_end_pose] + '.jpg'
		return img_name

	def save_img(self,img_url,img_name):
		print("Pic is requesting……")
		img = self.send_requests(img_url)
		time.sleep(5)
		file_name = img_name + '.jpg'
		print('pic is saving……')
		try:
			with open(img_name,'ab') as f:
				f.write(img.content)
		except Exception as e:
			raise e
		else:
			print("pic saved successefully!")
		
	def filter_out_img(self):
			all_img = self.get_all_img_url()
			current_path = self.mkdir(self.folder_path)
			print('current_path',current_path)
			goal_path = self.is_folder_Exists(current_path)
			file_names = self.get_files(self.folder_path)
			
			for img in all_img:
				i=1
				img_url = img['href']
				img_name = self.img_name(img_url)
				print('img_url:%s' % img_url)
				print('img_name:%s' % img_name)
				if goal_path:
					if img_name not in file_names:
						self.save_img(img_url,img_name)
						print('%s img downloaded！' % i)
					else:
						print("this img already in ……")
				i=i+1


if __name__ == '__main__':
	Images = dynamic_sbyder()
	#Images.filter_out_img()
	Images.get_all_answers()

	
