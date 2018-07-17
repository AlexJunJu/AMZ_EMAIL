#!/usr/bin/env python3
# _*_coding: utf-8 _*_
import datetime
import xlsxwriter

def bubble_sort():
	sort_list = [34,8,64,51,32,21] 
	element_cunts =len(sort_list)
	for i in range(0,element_cunts-1):
		for j in range(0,element_cunts-1-i):
			if sort_list[j]>sort_list[j+1]:
				sort_list[j],sort_list[j+1] = sort_list[j+1],sort_list[j]
	print(sort_list) 

def selection_sort():
	sort_list = [34,8,64,51,32,21] 
	element_cunts =len(sort_list)
	for i in range(0,element_cunts-1):
		for j in range(i+1,element_cunts):
			if sort_list[i]>sort_list[j]:
				sort_list[i],sort_list[j] = sort_list[j],sort_list[i]
				print("Round",i,":",sort_list)
	print(sort_list)

def straight_insertion_sort():
	sort_list = [34,8,64,51,32,21]
	element_cunts =len(sort_list)

	for i in range(0,element_cunts):

		if sort_list[i]<sort_list[i-1]:

			sortted_length = i-1
			temp = sort_list[i]
			sort_list[i] = sort_list[i-1]

			while (temp<sort_list[sortted_length] and sortted_length>=0):
				sort_list[sortted_length+1] = sort_list[sortted_length]
				sortted_length-=1
				print("Round",i,":",sort_list)
			sort_list[sortted_length+1]= temp

	print(sort_list)

def shell_sort():
	pass

def heap_sort():

	#exchange the lager value of heap and latter position
	def _swap_value(sort_list,i,j):
		sort_list[i],sort_list[j]= sort_list[j],sort_list[i]
		return sort_list

	#adjust to construct large heap
	def _adjust_heap(sort_list,start_node,end_node):

		temp = sort_list[start_node]
		i = start_node
		j = start_node*2
		
		while j<=end_node:
			if (j<end_node and
				sort_list[j]<sort_list[j+1]):
				j+=1
			if temp<sort_list[j]:
				sort_list[i] = sort_list[j]
				i = j
				j = 2*i
			else:
				break

		sort_list[i] = temp

	raw_list = [50, 16, 30, 10, 60,  90,  2, 80, 70]
	from collections import deque
	sort_list = deque(raw_list)
	sort_list.appendleft(0)

	sort_list_length = len(sort_list)-1
	first_non_leaf = sort_list_length//2
	
	for i in range(first_non_leaf):
		_adjust_heap(sort_list,first_non_leaf-i,sort_list_length)

	for i in range(sort_list_length-1):
		sort_list = _swap_value(sort_list, 1, sort_list_length-i)
		_adjust_heap(sort_list,1,sort_list_length-1-i)
	
	print (sort_list)






if __name__ == '__main__':

	#bubble_sort()
	#selection_sort()
	#straight_insertion_sort()
	heap_sort()
