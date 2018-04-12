from __future__ import absolute_import

import time
from random import randint
from selenium.webdriver.common.by import By
from .amz_base import AmzBase


class CheckoutCart(AmzBase):
    _cart_btn = (By.CSS_SELECTOR, '#nav-cart')
    _asin_checkout_btn = (By.CSS_SELECTOR, '#sc-buy-box-ptc-button')
    _asin_quantity = (By.NAME, 'quantity')

    _order_action_btn_us = (By.CSS_SELECTOR, '#orderSummaryPrimaryActionBtn')
    _order_delivery_form = (By.CSS_SELECTOR, '#shippingOptionFormId')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.asin = params.get('asin')
        self.market_place_id = params['market_place_id']
        self.email = account.get('email')

    def navigate(self):
        self.click(self._cart_btn, wait_time=10)
        return True

    def click_checkout(self):
        time.sleep(1 + randint(1, 4))
        self.select_by_value(self._asin_quantity, '1')

        time.sleep(3 + randint(1, 4))
        self.click(self._asin_checkout_btn, wait_time=5)

    def process(self):
        self.click_checkout()
