#!/usr/bin/env python3
import os
import time
#static requesr
import requests
#dynamic request
#import

#lib beautifulsoup4 and lxml can quickly  analyze html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class dynamic_sbyder():
	def __init__(self):
		self.Browser_Head_Agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
		#Given url and parameters
		self.web_url = 'http://unsplash.com'
		self.times = 10
		self.url_paras = {}
		self.folder_path = 'F:\program\syber_sbider\down_load_img'

	def browser_chrome(self):
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		web_deriver = webdriver.Chrome(chrome_options=chrome_options)
		return web_deriver

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
			time.sleep(5)
	
	def get_files(sself,folder_path):
		file_names = os.listdir(folder_path)
		return file_names

	def filter_out_img(self):
		print('start to send requests……')
		web_deriver = self.browser_chrome()
		web_deriver.get(self.web_url)
		self.scroll_down(deriver= web_deriver,times=self.times)
		all_img = BeautifulSoup(web_deriver.page_source,'lxml').findAll('img',itemprop="thumbnailUrl")
		current_path = self.mkdir(self.folder_path)
		print('current_path',current_path)
		goal_path = self.is_folder_Exists(current_path)
		file_names = self.get_files(self.folder_path)
		print("img标签的数量是：",len(all_img))
		for img in all_img:
			i=1
			img_url = img['srcset']
			#print("img标签的内容是：",img_url)
			first_pose = 0
			second_pose = img_url.index(' ',first_pose)
			img_url = img_url[first_pose:second_pose]
			print(img_url)
			name_start_pose = img_url.index('.com')+6
			name_end_pose = img_url.index('?')
			img_name = img_url[name_start_pose:name_end_pose] + '.jpg'
			#img_name = img_name.replace('/','')
			if goal_path:
				if img_name not in file_names:
					self.save_img(img_url,img_name)
					print('s% img downloaded！',i)
				else:
					print("this img already in ……")
			i=i+1

	def send_requests(self,web_url):
		print("Web Page Get requests Starts:")
		#send the target URL a get request,return a response object
		resp = requests.get(web_url)
		return resp

	def save_img(self,web_url,img_name):
		print("Pic is requesting……")
		img = self.send_requests(web_url)
		time.sleep(5)
		file_name = img_name + '.jpg'
		print('pic is saving……')
		with open(img_name,'ab') as f:
			f.write(img.content)
		print("pic saved successefully!")


if __name__ == '__main__':
	Images = dynamic_sbyder()
	Images.filter_out_img()


	
