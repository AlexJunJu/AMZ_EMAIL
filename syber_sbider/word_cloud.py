#!usr/bin/evn python3
from scipy.misc import imread
from wordcloud import WordCloud

file_path_english = 'C:/Users/ACEEC/Desktop/Game-of-Throne-E.txt'
file_path_chinese = 'C:/Users/ACEEC/Desktop/Game-of-Throne-C.txt'

def process_english():
	with open(file_path_english,'r', encoding='UTF-8') as f:
		text = f.read()
	return text

def process_chinese_with_para(str):
	import jieba
	text = "".join(jieba.cut(str))
	return text
	

def process_chinese():
	import jieba
	with open(file_path_chinese,'r', encoding='UTF-8') as f:
		original_text = f.read()
		text = "".join(jieba.cut(original_text))
		return text

# optional parameters of WordCloud()
# #Shape of WordCloud
# mask = ''
# background_color = 'white'
# max_words =2000
# font_path 
# #numbers of color
# random_state = 30
def generat_word_cloud(wordcloud_shape,font,text):
	#must instantiate before call function generate(text)
	word_cloud = WordCloud(
		mask = wordcloud_shape,
		background_color = 'black',
		font_path=font,
		)
	#generate function generates text cloud according the text
	word_cloud_img = word_cloud.generate(text)

	import matplotlib.pyplot as pyplot
	pyplot.imshow(word_cloud_img, interpolation='bilinear')
	pyplot.axis("off")
	pyplot.show()
	word_cloud.to_file("wordcloud.png")


wordcloud_shape = imread(r'C:/Users/ACEEC/Downloads/HF.jpg') 
# background_color  =  ''
# sacale = ''
# Shielding_words = ''
font = r'C:/Users/ACEEC/Downloads/font163/simheittf.ttf'

if __name__ == '__main__':
	text = process_chinese()
	generat_word_cloud(wordcloud_shape,font,text)
	print("ByeBye")


