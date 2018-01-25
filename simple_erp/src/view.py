#!/usr/bin/env python3
# _*_coding: utf-8 _*_
import datetime,time,os
import xlrd,xlsxwriter

from utils import ClosePort
from decimal import Decimal

from model import (AmzMarketplace,AmzWatchedAsin,AmzAsinInfoLog,AmzShipmentItem,
				   AmzShipmentInfo,AmzFbaInvInfo,AmzAsinReviewLog,AmzAsinBsrLog,
				   AmzSellerOrder,AmzDailyBusninessReport,AmzCostFeeLog,AmzTransactionInfo,
				   AmzProductCodeInfo,AmzSkuRelatedCode,BaseMethod)
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

	def append_new_asin():
		new_asin_list = AmzWatchedAsin.get_not_watched_asin()
		for marketplace_asin in new_asin_list:
			amz_watched_asin = AmzWatchedAsin()
			amz_watched_asin.account_id = 13
			amz_watched_asin.marketplace_id = marketplace_asin.marketplace_id
			amz_watched_asin.asin = marketplace_asin.asin
			amz_watched_asin.rule_list = '1111111111111111'
			amz_watched_asin.asin_status = 1
			amz_watched_asin.add(False)
		BaseMethod.commit()

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
		#append_new_asin()
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
			daily_info_list = [dailyInfo.marketplace_id,dailyInfo.name,
							   dailyInfo.asin,dailyInfo.sku,dailyInfo.fnsku,
							   dailyInfo.review_cnt,dailyInfo.review_date,
							   dailyInfo.available_qty,dailyInfo.reserved_qty,
							   dailyInfo.inventory_qty,dailyInfo.inbound_qty,
							   dailyInfo.average_orders_qty,dailyInfo.quantity_left_days,
							   dailyInfo.replenish_stock_qty,
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
		

	
		
	
	
		
