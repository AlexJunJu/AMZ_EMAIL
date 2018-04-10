#!/usr/bin/env python3
# _*_coding: utf-8 _*_
import datetime
import xlsxwriter

from model import (AmzSellerOrder,AmzCostFeeLog,AmzTransactionInfo,AmzProductCodeInfo,AmzSkuRelatedCode,BaseMethod)
from Objects import WeeklySalesInfo

# change Object type into list of 2_Dimension
def  _change_object_to_list(state_transaction_info_list):
	STATE_LIST = []
	for state_transaction in state_transaction_info_list:
		state_list = [state_transaction.marketplace_id,
					  state_transaction.name,
					  state_transaction.internal_code,
					  state_transaction.asin,
					  state_transaction.sku,
					  state_transaction.product_name,
					  state_transaction.fba_fulfillment_fee_per_unit,
					  state_transaction.quantity,
					  state_transaction.sales,
					  state_transaction.total_commission,
					  state_transaction.total_fba_fulfillment_fee,
					  state_transaction.station
					 ]
		STATE_LIST.append(state_list)
	return STATE_LIST

def  _change_datebase_result_to_object_list(state_transaction_info_list):
	STATE_LIST = []
	for state_transaction in state_transaction_info_list:
			weeklySalesInfo = WeeklySalesInfo()
			weeklySalesInfo.set_marketpalce_id(state_transaction.marketplace_id)
			weeklySalesInfo.set_name(state_transaction.name)
			weeklySalesInfo.set_asin(state_transaction.asin)
			weeklySalesInfo.set_sku(state_transaction.sku)
			weeklySalesInfo.set_fba_fulfillment_fee_per_unit(state_transaction.fba_fulfillment_fee_per_unit)
			weeklySalesInfo.set_quantity(state_transaction.quantity)
			weeklySalesInfo.set_sales(state_transaction.sales)
			weeklySalesInfo.set_total_commission(state_transaction.total_commission)
			weeklySalesInfo.set_total_fba_fulfillment_fee(state_transaction.total_fba_fulfillment_fee)
			weeklySalesInfo.set_tstation(state_transaction.station)
			STATE_LIST.append(weeklySalesInfo)
	return STATE_LIST

def _merge_trans_info_into_one_list(main_trans_info_list,states_list_of_trans_info):
	for trans_info_list in states_list_of_trans_info:
		for trans_info in trans_info_list:
			# must use iterator,or will repeat
			if (trans_info.asin,trans_info.sku) not in [(main_trans_info.asin,main_trans_info.sku)
														for main_trans_info in main_trans_info_list]:
				main_trans_info_list.append(trans_info)
	return main_trans_info_list

def _sum_QSCF_by_commen_asin_sku(main_trans_info_list,states_list_of_trans_info):
	# traverse side state
	for trans_info_list in states_list_of_trans_info:
		for trans_info in trans_info_list:

			for main_trans_info in main_trans_info_list:
				# judging condition should be careful
				if (main_trans_info.asin == trans_info.asin
				    and main_trans_info.sku == trans_info.sku
				   	and main_trans_info.marketplace_id != trans_info.marketplace_id
				   	and main_trans_info.station != trans_info.station
				   ):
					if main_trans_info.quantity and trans_info.quantity:
						main_trans_info.quantity+=trans_info.quantity
					if main_trans_info.sales and trans_info.sales:
						main_trans_info.sales+=trans_info.sales
					if main_trans_info.total_commission and trans_info.total_commission:
						main_trans_info.total_commission+=trans_info.total_commission
					if main_trans_info.total_fba_fulfillment_fee and trans_info.total_fba_fulfillment_fee:
						main_trans_info.total_fba_fulfillment_fee+=trans_info.total_fba_fulfillment_fee

	MainTransInfoList = _change_object_to_list(main_trans_info_list)
	return MainTransInfoList


def _weekly_logics():
	sales_info_list = AmzSellerOrder.get_weekly_sales_info()
	WeeklyInfoList = []
	for sales_info in sales_info_list:
		weeklySalesInfo = WeeklySalesInfo()
		weeklySalesInfo.set_marketpalce_id(sales_info.marketplace_id)
		weeklySalesInfo.set_name(sales_info.name)
		weeklySalesInfo.set_asin(sales_info.asin)
		weeklySalesInfo.set_sku(sales_info.sku)
		weeklySalesInfo.set_fba_fulfillment_fee_per_unit(sales_info.fba_fulfillment_fee_per_unit)
		weeklySalesInfo.set_quantity(sales_info.quantity)
		weeklySalesInfo.set_sales(sales_info.sales)
		weeklySalesInfo.set_total_commission(sales_info.total_commission)
		weeklySalesInfo.set_total_fba_fulfillment_fee(sales_info.total_fba_fulfillment_fee)
		weeklySalesInfo.set_tstation(sales_info.station)
		WeeklyInfoList.append(weeklySalesInfo)

	sku_code_list = AmzSkuRelatedCode.get_all()
	for weeklyInfo in WeeklyInfoList:
		for sku_code in sku_code_list:
			if weeklyInfo.sku == sku_code.sku:
				weeklyInfo.set_internal_code(sku_code.internal_code_for_product)

	name_sku_code_list = AmzProductCodeInfo.get_all()
	for weeklyInfo in WeeklyInfoList:
		for name_sku_code in name_sku_code_list:
			if weeklyInfo.internal_code == name_sku_code.internal_code_for_product:
				weeklyInfo.set_product_name(name_sku_code.internal_name_for_product)

	return WeeklyInfoList

def weekly_transaction_statistics_by_state():
	ye_list = []

	us_list = []

	ca_list = []

	uk_list = []

	de_list = [] 
	E4List = []

	fr_list = []
	E3List = []

	it_list = []

	es_list = []
		
	WeeklyInfoList = _weekly_logics()
	for weeklyInfo in WeeklyInfoList:
		if weeklyInfo.name == 'Yerongzhen' and weeklyInfo.station.replace(' ','') == 'com':
			ye_list.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') == 'com':
			us_list.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') == 'ca':
			ca_list.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') in ('co.uk'):
			uk_list.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') == 'de':
			#results returned by datebase is list of 2 dimension in which attribute can not be set
			de_list.append(weeklyInfo)
			E4List.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') == 'fr':
			fr_list.append(weeklyInfo)
			E3List.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') == 'it':
			it_list.append(weeklyInfo)
		if weeklyInfo.name == 'KingLove' and weeklyInfo.station.replace(' ','') == 'es':
			es_list.append(weeklyInfo)

		state_2_trans_list = {
							"YEList":ye_list,
							"USList":us_list,
							"CAList":ca_list,
							"UKList":uk_list,
							"DEList":de_list,
							"FRList":fr_list,
							"ITList":it_list,
							"ESList":es_list,
							"E3List":E3List,
							"E4List":E4List
							}

	return state_2_trans_list



def write_into_xlsx(state_dic):

	def _write_into_sheet(state_transaction_info_list_name,state_transaction_info_list):
		sheet_name = state_transaction_info_list_name[:2]
		if len(state_transaction_info_list)!=0:
			state_sheet = Workbook.add_worksheet(sheet_name)
			state_sheet.set_column('A:I',20)
			state_sheet.write(0,0,'marketplace_id')
			state_sheet.write(0,1,'name')
			state_sheet.write(0,2,'internal_code')
			state_sheet.write(0,3,'asin')
			state_sheet.write(0,4,'sku')
			state_sheet.write(0,5,'product_name')
			state_sheet.write(0,6,'fba_fulfillment_fee_per_unit')
			state_sheet.write(0,7,'quantity')
			state_sheet.write(0,8,'sales')
			state_sheet.write(0,9,'total_commission')
			state_sheet.write(0,10,'total_fba_fulfillment_fee')
			state_sheet.write(0,11,'station')
			StateRows = len(state_transaction_info_list)
			StateCols = len(state_transaction_info_list[0])
			for stateRow in range(1,StateRows+1):
				for stateCol in range(0,StateCols):
					if state_transaction_info_list[0][11]:
						state_sheet.write(stateRow,stateCol,state_transaction_info_list[stateRow-1][stateCol])
					else:
						continue

	# process the other europe three states
	def _the_other_europe_3_states(E3List,ITList,ESList):
		STATES_LIST = [ITList,ESList]
		E3List = _merge_trans_info_into_one_list(E3List,STATES_LIST)
		# from ipdb import set_trace
		# set_trace()
		EFList = _sum_QSCF_by_commen_asin_sku(E3List,STATES_LIST)
		_write_into_sheet("EFList",EFList)

	# process europe four states
	def _all_europe_4_states(E4List,E3List): 
		STATES_LIST = [E3List]
		E4List = _merge_trans_info_into_one_list(E4List,STATES_LIST)
		EUList = _sum_QSCF_by_commen_asin_sku(E4List,STATES_LIST)
		_write_into_sheet("EUList",EUList)


	Workbook = xlsxwriter.Workbook('./%s-%s.xlsx' % ((datetime.datetime.now().year,datetime.datetime.now().month-1)))	
	_write_into_sheet("YEList",_change_object_to_list(state_dic["YEList"]))
	_write_into_sheet("USList",_change_object_to_list(state_dic["USList"]))
	_write_into_sheet("CAList",_change_object_to_list(state_dic["CAList"]))
	_write_into_sheet("UKList",_change_object_to_list(state_dic["UKList"]))
	_write_into_sheet("DEList",_change_object_to_list(state_dic["DEList"]))
	_write_into_sheet("FRList",_change_object_to_list(state_dic["FRList"]))
	_write_into_sheet("E3List",_change_object_to_list(state_dic["E3List"]))
	_write_into_sheet("ITList",_change_object_to_list(state_dic["ITList"]))
	_write_into_sheet("ESList",_change_object_to_list(state_dic["ESList"]))
	
	_the_other_europe_3_states(state_dic["E3List"],
							   state_dic["ITList"],
							   state_dic["ESList"])
	
	_all_europe_4_states(state_dic["E4List"],
						 state_dic["E3List"],)
	
	#E3List,FRList,ITList,of this moment/here has been changed 
	# _write_into_sheet("E6List",_change_object_to_list(state_dic["E3List"]))
	# _write_into_sheet("f1List",_change_object_to_list(state_dic["FRList"]))
	# _write_into_sheet("i1List",_change_object_to_list(state_dic["ITList"]))
	# _write_into_sheet("e1List",_change_object_to_list(state_dic["ESList"]))
	# _write_into_sheet("e4List",_change_object_to_list(state_dic["E4List"]))
	#_all_europe_4_states(E4List,fr_list,
						 #it_list,es_list)		
	Workbook.close()

def get_bsr_ranks():
	seller_rank_info_list = AmzAsinBsrLog.query_latest_best_seller_rank()
	for dailyInfo in Daily_Info_List:
		for seller_rank_info in seller_rank_info_list:
			if (dailyInfo.marketplace_id == seller_rank_info.marketplace_id
				and dailyInfo.asin == seller_rank_info.asin
				and seller_rank_info.seller_ranks):
				dailyInfo.set_seller_ranks(seller_rank_info.seller_ranks)
	return Daily_Info_List

def get_review_info()
	review_info_list = AmzAsinReviewLog.query_latest_review_cnt()
	for dailyInfo in Daily_Info_List:
		for review_info in review_info_list:
			if ((dailyInfo.marketplace_id == review_info.marketplace_id)
				and	(dailyInfo.asin == review_info.asin)
				and review_info.review_cnt):
				dailyInfo.set_review_cnt(review_info.review_cnt)
				dailyInfo.set_review_date(review_info.latest_create_date)
	return Daily_Info_List


if __name__ == '__main__':

	states_tuple_of_trans_info = weekly_transaction_statistics_by_state()	
	write_into_xlsx(states_tuple_of_trans_info)
	print('byebye')