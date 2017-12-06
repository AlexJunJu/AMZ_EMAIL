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
from Objects import DailyInfo,MothlySalesInfo


#from DataBaseConnectionClass import Database_Connection


class ViewClass(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass
		
	@staticmethod
	def daily_info_list():
		

		#创建一个Daily_Info_List
		Marketplace_Id_Asin_List = []
		try:
			#___________________________________________________获取各站所对应的markeplace_id、website
			
			Marketplace_Id_List =[]
			Marketplaces_List = []

			Marketplace_Info = AmzMarketplace.get_all()
			for marketplace_info in Marketplace_Info:
				if marketplace_info.id and \
				   marketplace_info.market_place and \
				   marketplace_info.website :
					Marketplace_Id_List.append(marketplace_info.id)

					marketplace = AmzMarketplace()
					marketplace.id = marketplace_info.id
					marketplace.website = marketplace_info.website
					Marketplaces_List.append(marketplace)

			

			Daily_Info_List = []

			Watched_Fba_Markertplace_Id_Asin_Sku_Info = AmzWatchedAsin.get_watched_fba_marketplace_id_asin_sku_asc()
			for WarchedFbaMarketplaceIdAsinSKU in Watched_Fba_Markertplace_Id_Asin_Sku_Info:
				dailyInfo = DailyInfo()
				dailyInfo.set_marketpalce_id(WarchedFbaMarketplaceIdAsinSKU.marketplace_id)
				dailyInfo.set_name(WarchedFbaMarketplaceIdAsinSKU.name),
				dailyInfo.set_asin(WarchedFbaMarketplaceIdAsinSKU.asin)
				dailyInfo.set_sku(WarchedFbaMarketplaceIdAsinSKU.sku)
				Daily_Info_List.append(dailyInfo)



			Inv_Info = AmzFbaInvInfo.query_latest_fba_inv_info_order_by_nanme_desc()
			for dailyInfo in Daily_Info_List:
				# dailyInfo.set_fnsku(None)
				# dailyInfo.set_available_qty(0)
				# dailyInfo.set_reserved_qty(0)
				# dailyInfo.set_inventory_qty(0)

				for invinfo in Inv_Info:
					if (invinfo.marketplace_id in Marketplace_Id_List) and \
						invinfo.name == dailyInfo.name and \
						invinfo.asin == dailyInfo.asin and invinfo.sku == dailyInfo.sku:

						dailyInfo.set_fnsku(invinfo.fnsku)
						dailyInfo.set_available_qty(invinfo.quantity_available)
						dailyInfo.set_reserved_qty(invinfo.reserved_qty)
						dailyInfo.set_inventory_qty(invinfo.inventory_qty)
						



			Shipment_Info = AmzShipmentItem.query_shipment_info()
			for dailyInfo in Daily_Info_List:
				# dailyInfo.set_inbound_qty(0)
				for shipment in Shipment_Info:

					if((shipment.marketplace_id in Marketplace_Id_List) and \
						dailyInfo.name == shipment.name and \
						dailyInfo.sku == shipment.sku and \
						dailyInfo.fnsku == shipment.fnsku and shipment.inbound_qty):	
						# dailyInfo.set_shipped_qty(shipment.qty_shipped)
						# dailyInfo.set_received_qty(shipment.qty_received)
						dailyInfo.set_inbound_qty(shipment.inbound_qty)
					



			Review_Info = AmzAsinReviewLog.query_latest_review_cnt()
			for dailyInfo in Daily_Info_List:
				# dailyInfo.set_review_cnt(None)
				# dailyInfo.set_review_date(19990909)
				for review in Review_Info:
					# if ((dailyInfo.marketplace_id == review.marketplace_id) and  (dailyInfo.asin == review.asin) and review.review_cnt):
					# 由于各站点的markeplace_id不一致导致暂时只能用asin来确定，待斟酌  
					if ((dailyInfo.marketplace_id == review.marketplace_id) and \
						(dailyInfo.asin == review.asin)  and  \
						review.review_cnt):
						dailyInfo.set_review_cnt(review.review_cnt)
						dailyInfo.set_review_date(review.latest_create_date)
						


			Best_Seller_Rank = AmzAsinBsrLog.query_Latest_Bsr_Rank()
			for dailyInfo in Daily_Info_List:
				# dailyInfo.set_seller_ranks(None)
				for sranks in Best_Seller_Rank:
					if (dailyInfo.marketplace_id == sranks.marketplace_id and \
						dailyInfo.asin == sranks.asin and sranks.seller_ranks):
	
						dailyInfo.set_seller_ranks(sranks.seller_ranks)




			# Marketplaceid_Asin_orders_cnt = AmzSellerOrder.query_latest_week_average_daily_orders_qty()
			# for dailyInfo in Daily_Info_List:
			# 	dailyInfo.set_average_orders_qty(0)
			# 	for orders in Marketplaceid_Asin_orders_cnt:

			# 		if ((orders.marketplace_id in Marketplace_Id_List) and \
			# 			dailyInfo.asin == orders.asin and \
			# 			dailyInfo.sku == orders.sku and orders.average_orders_qty):

			# 			dailyInfo.set_average_orders_qty(orders.average_orders_qty)
			
			Marketplaceid_Asin_orders_cnt = AmzSellerOrder.query_average_daily_orders_qty()
			for dailyInfo in Daily_Info_List:
				for orders in Marketplaceid_Asin_orders_cnt:
					if ((orders.marketplace_id in Marketplace_Id_List) and
						dailyInfo.asin == orders.asin and
						dailyInfo.sku == orders.sku):
						dailyInfo.set_average_orders_qty_with_weight(orders.last_week_quantity,
																	 orders.fortnight_quantity,
																	 orders.month_quantity
																	)

			for dailyInfo in Daily_Info_List:
				dailyInfo.set_quantity_left_days(dailyInfo.inventory_qty,dailyInfo.inbound_qty,dailyInfo.average_orders_qty)
				dailyInfo.set_replenish_stock_qty(dailyInfo.inventory_qty,dailyInfo.inbound_qty,dailyInfo.average_orders_qty)	
				#dailyInfo.replenish_stock_qty(dailyInfo.inventory_qty,dailyInfo.inbound_qty,dailyInfo.average_orders_qty)



			return Daily_Info_List
			print("byebye")
		except Exception as e:
			raise

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
	def business_report():
		

		DailyBusinessReportList = []
		try:
			BusinessReportList=AmzDailyBusninessReport.get_all()

			for BusinessReport in BusinessReportList:
				#print(BusinessReport.marketplace_id,BusinessReport.parent_asin,BusinessReport.child_asin,BusinessReport.ordered_product_sales,BusinessReport.report_date)
				dailyBusinessReport = DailyBusinessReport()
				dailyBusinessReport.set_marketpalce_id(BusinessReport.marketplace_id)
				dailyBusinessReport.set_parent_asin(BusinessReport.parent_asin)
				dailyBusinessReport.set_child_asin(BusinessReport.child_asin)
				dailyBusinessReport.set_title(BusinessReport.title)
				dailyBusinessReport.set_sessions(BusinessReport.sessions)
				dailyBusinessReport.set_session_percentage(BusinessReport.session_percentage)
				dailyBusinessReport.set_page_views(BusinessReport.page_views)
				dailyBusinessReport.set_page_views_percentage(BusinessReport.page_views_percentage)
				dailyBusinessReport.set_buy_box_percentage(BusinessReport.buy_box_percentage)
				dailyBusinessReport.set_units_ordered(BusinessReport.units_ordered)
				dailyBusinessReport.set_unit_session_percentage(BusinessReport.unit_session_percentage)
				dailyBusinessReport.set_total_order_items(BusinessReport.total_order_items)
				dailyBusinessReport.set_ordered_product_sales(BusinessReport.ordered_product_sales)
				DailyBusinessReportList.append(dailyBusinessReport)

			return BusinessReportList

			
		except Exception as e:
			raise e
			



	@staticmethod
	def monthly_background_income_statistics_csv():


		Workbook = xlsxwriter.Workbook('./%s-%s.xlsx' % ((datetime.datetime.now().year,datetime.datetime.now().month-1)))
		
		# marketplace_suffix_list = []
		# MaketplaceList = AmzMarketplace.get_all()
		# for marketplace in MaketplaceList:
		# 	if marketplace.website:
		# 		print(marketplace.website[11:].replace(' ',''))
		# 		marketplace_suffix_list.append(marketplace.website[11:].replace(' ',''))

		COMList = []
		CAList  = []
		DEList  = []
		FRList  = []
		ITList  = []
		ESList  = []
		EUList  = []
		UKList= []
		SalesInfo = AmzSellerOrder.get_monthly_sales_info()

		for salesInfo in SalesInfo:
			monthlySalesInfo = MothlySalesInfo()
			monthlySalesInfo.set_marketpalce_id(salesInfo.marketplace_id)
			monthlySalesInfo.set_asin(salesInfo.asin)
			monthlySalesInfo.set_sku(salesInfo.sku)
			monthlySalesInfo.set_fba_fulfilment_fee_per_unit(salesInfo.fba_fulfilment_fee_per_unit)
			monthlySalesInfo.set_quantity(salesInfo.quantity)
			monthlySalesInfo.set_sales(salesInfo.sales)
			monthlySalesInfo.set_total_commission(salesInfo.total_commission)
			monthlySalesInfo.set_total_fba_fulfilment_fee(salesInfo.total_fba_fulfilment_fee)
			monthlySalesInfo.set_tstation(salesInfo.station)
			if salesInfo.station.replace(' ','') == 'com':
				COMList.append(salesInfo)

			if salesInfo.station.replace(' ','') == 'ca':
				CAList.append(salesInfo)

			if salesInfo.station.replace(' ','') == 'de':
				DEList.append(monthlySalesInfo)

			if salesInfo.station.replace(' ','') == 'fr':
				FRList.append(monthlySalesInfo)

			if salesInfo.station.replace(' ','') == 'it':
				ITList.append(monthlySalesInfo)

			if salesInfo.station.replace(' ','') == 'es':
				ESList.append(monthlySalesInfo)

			if salesInfo.station.replace(' ','') in ('co.uk'):
				UKList.append(salesInfo)

		
		if len(COMList)!=0:
			com_sheet = Workbook.add_worksheet('com')
			com_sheet.set_column('A:I',20)
			com_sheet.write(0,0,'marketplace_id')
			com_sheet.write(0,1,'asin')
			com_sheet.write(0,2,'sku')
			com_sheet.write(0,3,'fba_fulfilment_fee_per_unit')
			com_sheet.write(0,4,'quantity')
			com_sheet.write(0,5,'sales')
			com_sheet.write(0,6,'total_commission')
			com_sheet.write(0,7,'total_fba_fulfilment_fee')
			com_sheet.write(0,8,'station')
			COMrows = len(COMList)
			COMcols = len(COMList[0])
			for comRow in range(1,COMrows+1):
				for comCol in range(0,COMcols):
					if COMList[0][8] == 'com':
						com_sheet.write(comRow,comCol,COMList[comRow-1][comCol])
					else:
						continue


		if len(CAList)!=0:
			ca_sheet = Workbook.add_worksheet('CA')
			ca_sheet.set_column('A:I',20)
			ca_sheet.write(0,0,'marketplace_id')
			ca_sheet.write(0,1,'asin')
			ca_sheet.write(0,2,'sku')
			ca_sheet.write(0,3,'fba_fulfilment_fee_per_unit')
			ca_sheet.write(0,4,'quantity')
			ca_sheet.write(0,5,'sales')
			ca_sheet.write(0,6,'total_commission')
			ca_sheet.write(0,7,'total_fba_fulfilment_fee')
			ca_sheet.write(0,8,'station')
			CArows = len(CAList)
			CAcols = len(CAList[0])
			for caRow in range(1,CArows+1):
				for caCol in range(0,CAcols):
					if CAList[0][8] == 'ca':
						ca_sheet.write(caRow,caCol,CAList[caRow-1][caCol])
					else:
						continue



		for frList in FRList:
			if (frList.asin,frList.sku) not in [(deList.asin,deList.sku) for deList in DEList]:
				DEList.append(frList)

		for itList in ITList:
			if (itList.asin,itList.sku) not in [(deList.asin,deList.sku) for deList in DEList]:
				DEList.append(itList)

		for esList in ESList:
			if (esList.asin,esList.sku) not in [(deList.asin,deList.sku) for deList in DEList]:
				DEList.append(esList)

		for deList in DEList:
			for frList in FRList:
				if deList.marketplace_id !=frList.marketplace_id and \
				   deList.asin == frList.asin and deList.sku == frList.sku and deList.station != frList.station:
					deList.quantity+=frList.quantity
					deList.sales+=frList.sales
					deList.total_commission+=frList.total_commission
					deList.total_fba_fulfilment_fee+=frList.total_fba_fulfilment_fee

			for itList in ITList:
				if deList.marketplace_id != itList.marketplace_id and \
				   deList.asin == itList.asin and deList.sku == itList.sku and deList.station != itList.station:
					deList.quantity+=itList.quantity
					deList.sales+=itList.sales
					if deList.total_commission and itList.total_commission :
						deList.total_commission+=itList.total_commission
					if deList.total_fba_fulfilment_fee and itList.total_fba_fulfilment_fee :
						deList.total_fba_fulfilment_fee+=itList.total_fba_fulfilment_fee
				
			for esList in ESList:
				if deList.marketplace_id != esList.marketplace_id and \
				   deList.asin == esList.asin and deList.sku == esList.sku and deList.station != esList.station:
					deList.quantity+=esList.quantity
					deList.sales+=esList.sales
					deList.total_commission+=esList.total_commission
					if deList.total_fba_fulfilment_fee and esList.total_fba_fulfilment_fee:
						deList.total_fba_fulfilment_fee+=esList.total_fba_fulfilment_fee
			

			eulist = [deList.marketplace_id, deList.asin,deList.sku,\
					  deList.fba_fulfilment_fee_per_unit,deList.quantity,\
					  deList.sales,deList.total_commission,\
					  deList.total_fba_fulfilment_fee,\
					  deList.station
					 ]
			EUList.append(eulist)

		if len(EUList)!=0:
			eu_sheet = Workbook.add_worksheet('EU')
			eu_sheet.set_column('A:I',20)
			eu_sheet.write(0,0,'marketplace_id')
			eu_sheet.write(0,1,'asin')
			eu_sheet.write(0,2,'sku')
			eu_sheet.write(0,3,'fba_fulfilment_fee_per_unit')
			eu_sheet.write(0,4,'quantity')
			eu_sheet.write(0,5,'sales')
			eu_sheet.write(0,6,'total_comission')
			eu_sheet.write(0,7,'total_fba_fulfilment_fee')
			eu_sheet.write(0,8,'station')
			EUrows = len(EUList)
			EUcols = len(EUList[0])
			for euRow in range(1,EUrows+1):
				for euCol in range(0,EUcols):
					if EUList[0][8] == 'de':
						eu_sheet.write(euRow,euCol,EUList[euRow-1][euCol])
					else:
						continue


		if len(UKList)!=0:
			uk_sheet = Workbook.add_worksheet('UK')
			uk_sheet.set_column('A:I',20)
			uk_sheet.write(0,0,'marketplace_id')
			uk_sheet.write(0,1,'asin')
			uk_sheet.write(0,2,'sku')
			uk_sheet.write(0,3,'fba_fulfilment_fee_per_unit')
			uk_sheet.write(0,4,'quantity')
			uk_sheet.write(0,5,'sales')
			uk_sheet.write(0,6,'total_comission')
			uk_sheet.write(0,7,'total_fba_fulfilment_fee')
			uk_sheet.write(0,8,'station')
			# print(len(UKList))
			# print(len(UKList[0]))
			Ukrows = len(UKList)
			Ukcols = len(UKList[0])
			for ukRow in range(1,Ukrows+1):
				for ukCol in range(0,Ukcols):
					if UKList[0][8] == 'co.uk':
						uk_sheet.write(ukRow,ukCol,UKList[ukRow-1][ukCol])
					else:
						continue

				
		Workbook.close()

		print('byebye')
		
	
	
		
