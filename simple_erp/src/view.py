#!/usr/bin/env python3
# _*_coding: utf-8 _*_
import datetime,time,os
import xlrd,xlsxwriter

from utils import ClosePort
from decimal import Decimal

from model import (AmzMarketplace,AmzWatchedAsin,AmzAsinInfoLog,AmzShipmentItem,
				   AmzShipmentInfo,AmzFbaInvInfo,AmzAsinReviewLog,AmzAsinBsrLog,
				   AmzSellerOrder,AmzDailyBusninessReport,AmzCostFeeLog,AmzTransactionInfo,
				   BaseMethod)
from Objects import DailyInfo,WeeklySalesInfo


#from DataBaseConnectionClass import Database_Connection
class ViewClass(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass

	def get_marketplace_info(self):
		marketplace_list = []
		marketplace_id_list = []
		marketplace_info_list = AmzMarketplace.get_all()
		for marketplace_info in marketplace_info_list:
			if (marketplace_info.id 
			   and marketplace_info.market_place 
			   and marketplace_info.website):
				marketplace_id_list.append(marketplace_info.id)
				marketplace = AmzMarketplace()
				marketplace.id = marketplace_info.id
				marketplace.website = marketplace_info.website
				#marketplace_list.append(marketplace)
		return marketplace_id_list

	def get_watched_fba_marketplace_id_asin_sku(self,Daily_Info_List):
		watched_id_asin_sku_list =AmzWatchedAsin.get_watched_fba_marketplace_id_asin_sku_asc()
		for watched_id_asin_sku in watched_id_asin_sku_list:
			dailyInfo = DailyInfo()
			dailyInfo.set_marketpalce_id(watched_id_asin_sku.marketplace_id)
			dailyInfo.set_name(watched_id_asin_sku.name),
			dailyInfo.set_asin(watched_id_asin_sku.asin)
			dailyInfo.set_sku(watched_id_asin_sku.sku)
			Daily_Info_List.append(dailyInfo)
		return Daily_Info_List

	def query_latest_fba_inv_info_order_by_nanme(self,Daily_Info_List,marketplace_id_list):
		inventory_info_list = AmzFbaInvInfo.query_latest_fba_inv_info_order_by_name_desc()
		for dailyInfo in Daily_Info_List:
			for inventory_info in inventory_info_list:
				if ((inventory_info.marketplace_id in marketplace_id_list)
					and inventory_info.name == dailyInfo.name 
					and inventory_info.asin == dailyInfo.asin 
					and inventory_info.sku == dailyInfo.sku):
						dailyInfo.set_fnsku(inventory_info.fnsku)
						dailyInfo.set_available_qty(inventory_info.quantity_available)
						dailyInfo.set_reserved_qty(inventory_info.reserved_qty)
						dailyInfo.set_inventory_qty(inventory_info.inventory_qty)
		return Daily_Info_List

	def query_shipment_info(self,Daily_Info_List,marketplace_id_list):
		shipment_info_list = AmzShipmentItem.query_shipment_info()
		for dailyInfo in Daily_Info_List:
			for shipment_info in shipment_info_list:
				if((shipment_info.marketplace_id in marketplace_id_list) 
					and dailyInfo.name == shipment_info.name 
					and dailyInfo.sku == shipment_info.sku 
					and dailyInfo.fnsku == shipment_info.fnsku 
					and shipment_info.inbound_qty):	
						dailyInfo.set_inbound_qty(shipment_info.inbound_qty)
		return Daily_Info_List

	def query_latest_review_cnt(self,Daily_Info_List):
		review_info_list = AmzAsinReviewLog.query_latest_review_cnt()
		for dailyInfo in Daily_Info_List:
			for review_info in review_info_list:
				if ((dailyInfo.marketplace_id == review_info.marketplace_id) 
					and	(dailyInfo.asin == review_info.asin) 
					and review_info.review_cnt):
					dailyInfo.set_review_cnt(review_info.review_cnt)
					dailyInfo.set_review_date(review_info.latest_create_date)
		return Daily_Info_List

	def  query_latest_best_seller_rank(self,Daily_Info_List):
		seller_rank_info_list = AmzAsinBsrLog.query_latest_best_seller_rank()
		for dailyInfo in Daily_Info_List:
			for seller_rank_info in seller_rank_info_list:
				if (dailyInfo.marketplace_id == seller_rank_info.marketplace_id 
					and dailyInfo.asin == seller_rank_info.asin 
					and seller_rank_info.seller_ranks):
					dailyInfo.set_seller_ranks(seller_rank_info.seller_ranks)
		return Daily_Info_List

	def query_average_daily_orders_qty(self,Daily_Info_List,marketplace_id_list):
		average_daily_orders_info_list = AmzSellerOrder.query_average_daily_orders_qty()
		for dailyInfo in Daily_Info_List:
			for order_info in average_daily_orders_info_list:
				if ((order_info.marketplace_id in marketplace_id_list) 
					and	dailyInfo.asin == order_info.asin 
					and	dailyInfo.sku == order_info.sku):
					dailyInfo.set_average_orders_qty_with_weight(order_info.last_week_quantity,
																 order_info.fortnight_quantity,
																 order_info.month_quantity
																)
		return Daily_Info_List

	def set_available_days_and_replenishment_qty(self,Daily_Info_List):
		for dailyInfo in Daily_Info_List:
			dailyInfo.set_quantity_left_days(dailyInfo.inventory_qty,dailyInfo.inbound_qty,dailyInfo.average_orders_qty)
			dailyInfo.set_replenish_stock_qty(dailyInfo.inventory_qty,dailyInfo.inbound_qty,dailyInfo.average_orders_qty)	
		return Daily_Info_List

	def daily_info_list_new(self):
		marketplace_id_list = self.get_marketplace_info()
		Daily_Info_List = []
		self.get_watched_fba_marketplace_id_asin_sku(Daily_Info_List)
		self.query_latest_fba_inv_info_order_by_nanme(Daily_Info_List,marketplace_id_list)
		self.query_shipment_info(Daily_Info_List,marketplace_id_list)
		self.query_latest_review_cnt(Daily_Info_List)
		self.query_latest_best_seller_rank(Daily_Info_List)
		self.query_average_daily_orders_qty(Daily_Info_List,marketplace_id_list)
		self.set_available_days_and_replenishment_qty(Daily_Info_List)
		return Daily_Info_List

	@staticmethod
	def daily_info_xlsx():

		Daily_Info_List = ViewClass.daily_info_list()

		Workbook = xlsxwriter.Workbook('./%s.xlsx' % (datetime.datetime.now().strftime('%Y-%m-%d')))
		dailyinfo_sheet = Workbook.add_worksheet('DailyInfo')
		dailyinfo_sheet.set_column('A:O',20)
		dailyinfo_sheet.write(0,0,'Marketplace_id')
		dailyinfo_sheet.write(0,1,'name')
		dailyinfo_sheet.write(0,2,'ASIN')
		dailyinfo_sheet.write(0,3,'SKU')
		dailyinfo_sheet.write(0,4,'FNSKU')
		dailyinfo_sheet.write(0,5,'Review_Cnt')
		dailyinfo_sheet.write(0,6,'Review_Date')
		dailyinfo_sheet.write(0,7,'Availabele_Qty')
		dailyinfo_sheet.write(0,8,'Reserved_Qty')
		dailyinfo_sheet.write(0,9,'Inventory')
		dailyinfo_sheet.write(0,10,'Inbound')
		dailyinfo_sheet.write(0,11,'Average_Orders_Qty')
		dailyinfo_sheet.write(0,12,'Quantity_Left_Days')
		dailyinfo_sheet.write(0,13,'Replenish_Stock_Qty')
		dailyinfo_sheet.write(0,14,'Best_Seller_Rank')

		DailyInfo_List = []
		for dailyInfo in Daily_Info_List:
			daily_info_list = [dailyInfo.marketplace_id,dailyInfo.name,\
							   dailyInfo.asin,dailyInfo.sku,dailyInfo.fnsku,\
							   dailyInfo.review_cnt,dailyInfo.review_date,
							   dailyInfo.available_qty,dailyInfo.reserved_qty,\
							   dailyInfo.inventory_qty,dailyInfo.inbound_qty,\
							   dailyInfo.average_orders_qty,dailyInfo.quantity_left_days,\
							   dailyInfo.replenish_stock_qty,\
							   str(dailyInfo.seller_ranks).replace(',','\r\n')
							  ]
			# from ipdb import set_trace
			# set_trace()
			# print(str(dailyInfo.seller_ranks).replace(',','\r\n'))
			DailyInfo_List.append(daily_info_list)

		rows = len(DailyInfo_List)
		cols = len(DailyInfo_List[0])

		for row in range(1,rows+1):
			for col in range(0,cols):
				dailyinfo_sheet.write(row,col,DailyInfo_List[row-1][col])

		Workbook.close()
		print('byebye')
		


	@staticmethod
	def weekly_transaction_statistics_xlsx():
		YEList = []
		USList = []
		CAList = []
		UKList = []

		DEList = []
		E4List = []

		FRList = []
		E3List = []

		ITList = []
		ITList_FOR_SUM = []

		ESList = []
		ESList_FOR_SUM = []
		
		# change Object type into list of 2_Dimension
		def  _formate_datebase_record(state_transaction_info_list):
			STATE_LIST = []
			for state_transaction in state_transaction_info_list:
				state_list = [state_transaction.marketplace_id,
							  state_transaction.name,
							  state_transaction.asin,
							  state_transaction.sku,
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
					if (trans_info.asin,trans_info.sku) not in [(main_trans_info.asin,main_trans_info.sku)
																for main_trans_info in main_trans_info_list]:
						main_trans_info_list.append(trans_info)
			return main_trans_info_list

		def _sum_QSCF_by_commen_asin_sku(main_trans_info_list,states_list_of_trans_info):
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
							continue

			MainTransInfoList = _formate_datebase_record(main_trans_info_list)
			return MainTransInfoList

		def _write_into_sheet(state_transaction_info_list_name,state_transaction_info_list):
			sheet_name = state_transaction_info_list_name[:2]
			if len(state_transaction_info_list)!=0:
				state_sheet = Workbook.add_worksheet(sheet_name)
				state_sheet.set_column('A:I',20)
				state_sheet.write(0,0,'marketplace_id')
				state_sheet.write(0,1,'name')
				state_sheet.write(0,2,'asin')
				state_sheet.write(0,3,'sku')
				state_sheet.write(0,4,'fba_fulfillment_fee_per_unit')
				state_sheet.write(0,5,'quantity')
				state_sheet.write(0,6,'sales')
				state_sheet.write(0,7,'total_commission')
				state_sheet.write(0,8,'total_fba_fulfillment_fee')
				state_sheet.write(0,9,'station')
				StateRows = len(state_transaction_info_list)
				StateCols = len(state_transaction_info_list[0])
				for stateRow in range(1,StateRows+1):
					for stateCol in range(0,StateCols):
						if state_transaction_info_list[0][9]:
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
		def _all_europe_4_states(E4List,FRList,ITList,ESList): 
			STATES_LIST = [FRList,ITList,ESList]
			E4List = _merge_trans_info_into_one_list(E4List,STATES_LIST)
			EUList = _sum_QSCF_by_commen_asin_sku(E4List,STATES_LIST)
			_write_into_sheet("EUList",EUList)			

		SalesInfo = AmzSellerOrder.get_weekly_sales_info()
		for salesInfo in SalesInfo:
			weeklySalesInfo = WeeklySalesInfo()
			weeklySalesInfo.set_marketpalce_id(salesInfo.marketplace_id)
			weeklySalesInfo.set_name(salesInfo.name)
			weeklySalesInfo.set_asin(salesInfo.asin)
			weeklySalesInfo.set_sku(salesInfo.sku)
			weeklySalesInfo.set_fba_fulfillment_fee_per_unit(salesInfo.fba_fulfillment_fee_per_unit)
			weeklySalesInfo.set_quantity(salesInfo.quantity)
			weeklySalesInfo.set_sales(salesInfo.sales)
			weeklySalesInfo.set_total_commission(salesInfo.total_commission)
			weeklySalesInfo.set_total_fba_fulfillment_fee(salesInfo.total_fba_fulfillment_fee)
			weeklySalesInfo.set_tstation(salesInfo.station)

			if salesInfo.name == 'Yerongzhen' and salesInfo.station.replace(' ','') == 'com':
				YEList.append(salesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') == 'com':
				USList.append(salesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') == 'ca':
				CAList.append(salesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') in ('co.uk'):
				UKList.append(salesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') == 'de':
				#results returned by datebase is list of 2 dimension in which attribute can not be set
				DEList.append(salesInfo)
				E4List.append(weeklySalesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') == 'fr':
				FRList.append(salesInfo)
				E3List.append(weeklySalesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') == 'it':
				ITList.append(salesInfo)
				ITList_FOR_SUM.append(weeklySalesInfo)

			if salesInfo.name == 'KingLove' and salesInfo.station.replace(' ','') == 'es':
				ESList.append(salesInfo)
				ESList_FOR_SUM.append(weeklySalesInfo)

		Workbook = xlsxwriter.Workbook('./%s-%s.xlsx' % ((datetime.datetime.now().year,datetime.datetime.now().month-1)))
		_write_into_sheet("YEList",YEList)
		_write_into_sheet("USList",USList)
		_write_into_sheet("CAList",CAList)
		_write_into_sheet("UKList",UKList)
		_write_into_sheet("DEList",DEList)
		_write_into_sheet("FRList",FRList)
		_write_into_sheet("ITList",ITList)
		_write_into_sheet("ESList",ESList)
		_the_other_europe_3_states(E3List,ITList_FOR_SUM,ESList_FOR_SUM)
		#_write_into_sheet("E3List",_formate_datebase_record(E3List))
		# E3List of this moment/here has been changed 
		_all_europe_4_states(E4List,_change_datebase_result_to_object_list(FRList),ITList_FOR_SUM,ESList_FOR_SUM)		
		Workbook.close()
		print('byebye')
		
	
	
		
