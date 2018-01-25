#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from view import ViewClass 
import os
from model import AmzSellerOrder,AmzProductCodeInfo,AmzSkuRelatedCode

ViewClass.weekly_transaction_statistics_xlsx()
#Buyer_Order = AmzSellerOrder.get_buyer_email_by_payments_last_day()
#Buyer_Order = AmzSkuRelatedCode.get_all()
#print(len(Buyer_Order))

	
print('byebye')
os._exit(0)
