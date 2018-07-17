#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime,time,math,decimal





class DailyInfo(object):
	"""docstring for Prodcut"""

	# initialize attribute when create a new instance
	def __init__(self):
		#定义在__init__()方法里的变量就是实例属性，这些属性只有被创建实例时才会被创建。
		# self.marketplace_id = None
		# self.name = None
		# self.asin = None
		# self.sku = None
		self.fnsku = None
		self.review_cnt = None
		self.review_date = "~"
		self.available_qty = 0
		self.received_qty = 0
		self.inbound_qty = 0
		self.inventory_qty = 0
		self.seller_ranks = None
		self.average_orders_qty = 0


	def set_marketpalce_id(self,marketplace_id):
		if marketplace_id: 
			self.marketplace_id = marketplace_id
	def get_marketpalce_id(self):
			return self.marketplace_id

	def set_market_palce(self,market_place):
		if market_place: 
			self.market_place = market_place
	def get_market_palce(self):
			return self.market_place

	def set_name(self,name):
		if name:
			self.name=name 
	def get_name(self):
		return self.name
		
	def set_asin(self,asin):
		if asin :
			self.asin=asin 
	def get_asin(self):
		return self.asin

	def set_sku(self,sku):
		if sku :
			self.sku=sku 
	def get_sku(self):
		return self.sku

	def set_fnsku(self,fnsku):
		if fnsku :
			self.fnsku=fnsku
		else:
			self.fnsku = None
	def get_fnsku(self):
		return self.fnsku

	def set_average_orders_qty(self,average_orders_qty):
		if isinstance(average_orders_qty,int):
			self.average_orders_qty = average_orders_qty
		else:
			self.average_orders_qty = int(round(average_orders_qty))
	def get_average_orders_qty(self):
		return self.average_orders_qty

	def set_average_orders_qty_with_weight(self,week_average_orders_qty,fortnight_average_qty,month_average_qty):
		_WEEK_WEIGHT_3 = decimal.Decimal(0.4)
		_WEEK_WEIGHT_2 = decimal.Decimal(0.6)
		_WEEK_WEIGHT_1 = decimal.Decimal(1)

		_FOTNIGHT_WEIGHT_3 = decimal.Decimal(0.35)
		_FOTNIGHT_WEIGHT_2 = decimal.Decimal(0.4)

		_MONTHT_WEIGHT_3 =decimal.Decimal(0.25)

		if  (week_average_orders_qty and
		     fortnight_average_qty and
		     month_average_qty):
			
			self.average_orders_qty = round(week_average_orders_qty*_WEEK_WEIGHT_3+
										    fortnight_average_qty*_FOTNIGHT_WEIGHT_3+
										    month_average_qty*_MONTHT_WEIGHT_3
											)
		if  (week_average_orders_qty and
		    fortnight_average_qty and
		    month_average_qty is None):

			self.average_orders_qty = round(week_average_orders_qty*_WEEK_WEIGHT_2+
										   fortnight_average_qty*_FOTNIGHT_WEIGHT_2
										  )
		if  (week_average_orders_qty and
			fortnight_average_qty is None and
			month_average_qty is None):
			self.average_orders_qty = round(week_average_orders_qty*_WEEK_WEIGHT_1)	

	def get_average_orders_qty_with_weight(self):
		return self.average_orders_qty	


	def set_review_cnt(self,review_cnt):
		self.review_cnt=review_cnt 

	def get_review_cnt(self):
			return self.review_cnt

	def set_review_date(self,review_date):
		# if (review_date > (datetime.date.today()- datetime.timedelta(days=3))):
		#if (int(datetime.date.today().strftime('%Y%m%d'))-review_date<=2):
		if (datetime.date.today()-datetime.datetime.strptime('%d' %review_date, "%Y%m%d").date()).days <= 3:
			
			#print(datetime.date.today())
			#print(time.strptime('%d' %review_date, "%Y%m%d"))
			self.review_date=review_date
		else:
			self.review_date="~" 

	def get_review_date(self):
			return self.review_date


	def set_available_qty(self,available_qty):
		self.available_qty=available_qty 
	def get_available_qty(self):
		return self.available_qty

	def set_reserved_qty(self,reserved_qty):
		self.reserved_qty=reserved_qty 
	def get_reserved_qty(self):
		return self.reserved_qty

	def set_inventory_qty(self,inventory_qty):
		self.inventory_qty=inventory_qty 
	def get_inventory_qty(self):
		return self.inventory_qty

	def set_shipped_qty(self,shipped_qty):
		self.shipped_qty=shipped_qty 
	def get_shipped_qty(self):
		return self.shipped_qty

	def set_received_qty(self,received_qty):
		self.received_qty=received_qty 
	def get_received_qty(self):
		return self.received_qty



	def set_inbound_qty(self,inbound_qty):
		self.inbound_qty=inbound_qty 
	def get_inbound_qty(self):
		return self.inbound_qty

	def set_seller_ranks(self,seller_ranks):
		self.seller_ranks=seller_ranks 
	def get_seller_ranks(self):
		return self.seller_ranks      


	def set_quantity_left_days(self,inventory_qty,inbound_qty,average_orders_qty):
		_stock_warning_days = 24
		_notificaton_days = 5
		if (average_orders_qty != 0):
			if (inventory_qty+inbound_qty) //(average_orders_qty)-_stock_warning_days >_notificaton_days:
				self.quantity_left_days = '……'
			else:
				self.quantity_left_days = (inventory_qty+inbound_qty) //(average_orders_qty)-_stock_warning_days
		else:
			if (inventory_qty+inbound_qty)<_stock_warning_days:
				self.quantity_left_days = _stock_warning_days
			else:
				self.quantity_left_days= '……'
	def get_quantity_left_days(self):
		return self.quantity_left_days



	def set_replenish_stock_qty(self,inventory_qty,inbound_qty,average_orders_qty):
		_stock_reserved_days = 40
		_stock_warning_days = 24

		if (average_orders_qty != 0) :
			if (average_orders_qty*_stock_reserved_days-(inventory_qty+inbound_qty) >= 0 ):
				self.replenish_stock_qty = average_orders_qty*_stock_reserved_days-(inventory_qty+inbound_qty)
			else :
				self.replenish_stock_qty='……'	
		else :
			if ((inventory_qty+inbound_qty) <= _stock_warning_days):
				self.replenish_stock_qty = _stock_warning_days-(inventory_qty+inbound_qty)
			else :
				self.replenish_stock_qty='……'
	def get_replenish_stock_qty(self):
		return self.replenish_stock_qty  


class WeeklySalesInfo(object):
	"""docstring for DailyBusinessReport"""
	def __init__(self):
		self.product_name = ''
		

	def set_marketpalce_id(self,marketplace_id):
		if marketplace_id: 
			self.marketplace_id = marketplace_id
	def get_marketpalce_id(self):
			return self.marketplace_id

	def set_name(self,name):
		if name:
			self.name=name 
	def get_name(self):
		return self.name

	def set_product_name(self,product_name):
		if product_name:
			self.product_name=product_name 
	def get_product_name(self):
		return self.product_name

	def set_internal_code(self,internal_code):
		if internal_code:
			self.internal_code=internal_code 
	def get_internal_code(self):
		return self.internal_code

	def set_asin(self,asin):
		if asin: 
			self.asin = asin
	def get_asin(self):
			return self.asin

	def set_sku(self,sku):
		if sku: 
			self.sku = sku
	def get_sku(self):
			return self.sku

	def set_fba_fulfillment_fee_per_unit(self,fba_fulfillment_fee_per_unit):
			self.fba_fulfillment_fee_per_unit = fba_fulfillment_fee_per_unit
	def get_fba_fulfillment_fee_per_unit(self):
			return self.fba_fulfillment_fee_per_unit

	def set_quantity(self,quantity):
			self.quantity = quantity
	def get_quantity(self):
			return self.quantity


	def set_sales(self,sales):
			self.sales = sales
	def get_sales(self):
			return self.sales


	def set_total_commission(self,total_commission):
			self.total_commission = total_commission
	def get_total_commission(self):
			return self.atotal_commission


	def set_total_fba_fulfillment_fee(self,total_fba_fulfillment_fee):
			self.total_fba_fulfillment_fee = total_fba_fulfillment_fee
	def get_total_fba_fulfillment_fee(self):
			return self.total_fba_fulfillment_fee

	def set_tstation(self,station):
			self.station = station
	def get_station(self):
			return self.station
