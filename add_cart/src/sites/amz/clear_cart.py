from __future__ import absolute_import

import time
from random import randint
from selenium.webdriver.common.by import By
from .amz_base import AmzBase


class ClearCart(AmzBase):
    _home_cart = (By.ID, 'nav-cart')
    _cart_delete = [(By.XPATH, '//input[contains(@name, "submit.delete")]'),
                    (By.CSS_SELECTOR, 'input[value=Delete]')]

    _ignore_msgs = ['stale element reference', 'Element is not clickable']

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)

    def navigate(self):
        _cart_count = (By.ID, 'nav-cart-count')
        cart_count = self.find_element(*_cart_count)
        if cart_count:
            cart_count = self.wait_valid_element(_cart_count)
            if cart_count.text.strip() == "0":
                return False

        self.click(self._home_cart, wait_time=10)
        return True

    def _meet_ignorable_msg(self, err):
        for msg in self._ignore_msgs:
            if msg in err:
                return True

        return False

    def process(self):
        while True:
            time.sleep(4 + randint(1, 4))
            del_elem = self.find_alternative_elem(self._cart_delete)
            if not del_elem:
                return
            self.click_elem(del_elem, wait_time=5)
