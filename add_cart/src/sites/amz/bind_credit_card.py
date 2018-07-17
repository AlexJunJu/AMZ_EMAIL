from __future__ import absolute_import

import logging as log
import time
import random
from selenium.webdriver.common.by import By
from sites.exception import StepFailed
from .amz_base import AmzBase


class BindCreditCard(AmzBase):
    url_tmpl = 'https://{market}/gp/css/account/address/view.html' +\
        '?ie=UTF8&ref_=ya_add_address&viewID=newAddress'

    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]
    _acct_orders = (By.ID, 'your-orders-button-announce')

    _addr_user = (By.NAME, 'ppw-fullName')
    _addr_addr1 = (By.NAME, 'ppw-line1')
    _addr_addr2 = (By.NAME, 'ppw-line2')
    _addr_city = (By.NAME, 'ppw-city')
    _addr_state = (By.NAME, 'ppw-stateOrRegion')
    _addr_country = (By.NAME, 'ppw-countryCode')
    _addr_zip = (By.NAME, 'ppw-postalCode')
    _addr_phone = (By.NAME, 'ppw-phoneNumber')
    _addr_submit_btn = (By.NAME, 'ppw-widgetEvent:AddAddressEvent')

    _addr_suggst_btn = (By.NAME, 'ppw-widgetEvent:UseSuggestedAddressEvent')
    _addr_add_addr_btn = (By.NAME, 'ppw-widgetEvent:ShowAddAddressEvent')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.url = self.url_tmpl.format(**{'market': self.url})
        self.card_info = self.params.get('credit_card_info', {})
        self.addr_info = self.params.get('credit_card_addr_info', {})
        if not self.addr_info:
            self.addr_info = self.params.get('addr_info', {})

    def validate(self):
        if not self.card_info or not self.addr_info:
            return False
        return True
        # @TODO Need to check more in future

    def navigate(self):
        if not self.validate():
            raise self.make_step_failed('Invalid params')

        # goto account dashboard
        account_link = self.find_alternative_elem(self._nav_link_your_account)
        self.click_elem(account_link, wait_time=5)

        # goto payment
        self.click((By.XPATH, '//div[@data-card-identifier="PaymentOptions"]'),
                   wait_time=5)

        return True

    def add_card(self):
        # _card_confirm = (By.NAME, 'ppw-widgetEvent:AddCreditCardEvent')
        # elem = self.find_elements(*_card_confirm)
        # self.move_to_elem_js(elem)

        def _get_card_holder():
            _card_holder = (By.NAME, 'ppw-accountHolderName')
            for i in xrange(3):
                elems = self.find_elements(*_card_holder)
                for elem in elems:
                    if elem.is_enabled() and elem.is_displayed():
                        return elem
                time.sleep(1)
            else:
                return None

        # Wait until elem is enabled
        elem = _get_card_holder()
        if not elem:
            _expander = (
                By.XPATH,
                '//*[@id="cpefront-mpo-widget"]/div/div[2]/div/div[2]' +
                '/div/div[1]/div/div[1]/a')
            self.click(_expander)

            elem = _get_card_holder()
            if not elem:
                raise self.make_step_failed('Failed to add card')

        elem.send_keys(self.card_info.get('card_holder'))

        _card_number = (By.NAME, 'addCreditCardNumber')
        elem = self.wait_visible_element(_card_number)
        elem.send_keys(self.card_info.get('card_number'))

        expired_date = self.card_info.get('expired_date')
        tokens = expired_date.split('-')
        expired_date_year = tokens[0]
        expired_date_mon = tokens[1]
        _expired_year = (By.NAME, 'ppw-expirationDate_year')
        self.select_by_value(_expired_year, expired_date_year)
        _expired_mon = (By.NAME, 'ppw-expirationDate_month')
        self.select_by_value(_expired_mon, str(int(expired_date_mon)))

        _card_confirm = (By.NAME, 'ppw-widgetEvent:AddCreditCardEvent')
        self.click(_card_confirm)

        time.sleep(5 + random.randint(1, 4))

    def add_address(self):
        if self.is_visible(self._addr_add_addr_btn):
            self.click(self._addr_add_addr_btn)

        addr1 = self.wait_valid_element(self._addr_addr1, wait_time=5)
        addr2 = self.wait_valid_element(self._addr_addr2)
        city = self.wait_valid_element(self._addr_city)
        state = self.wait_valid_element(self._addr_state)
        addr_zip = self.wait_valid_element(self._addr_zip)
        phone = self.wait_valid_element(self._addr_phone)

        addr1.clear()
        addr1.send_keys(self.addr_info.get('address_line1'))
        if not self.addr_info.get('address_line1'):
            addr1.send_keys(self.addr_info.get('address_line2', ''))
        else:
            addr2.clear()
            addr2.send_keys(self.addr_info.get('address_line2', ''))
        city.clear()
        city.send_keys(self.addr_info.get('city'))

        state.clear()
        state.send_keys(self.addr_info.get('state'))
        addr_zip.clear()
        addr_zip.send_keys(self.addr_info.get('zip_code'))

        phone_num = self.card_info.get('telephone')
        if not phone_num:
            phone_num = self.account.get('telephone')
        phone.clear()
        phone.send_keys(phone_num)

        def _get_country():
            _country = (By.NAME, 'ppw-countryCode')
            for i in xrange(5):
                elems = self.find_elements(*_country)
                for elem in elems:
                    if elem.is_enabled() and elem.is_displayed():
                        return elem
                time.sleep(1)
            else:
                return None

        elem = _get_country()
        if not elem:
            raise self.make_step_failed('Failed to add addr to card')
        self.select_elem_by_value(elem, self.addr_info.get('country_code'))

        self.click(self._addr_submit_btn)
        time.sleep(4 + random.randint(1, 4))

    def post_add_address(self):
        addr_suggst_btn = self.find_element(*self._addr_suggst_btn)
        if not addr_suggst_btn:
            return

        self.click(self._addr_suggst_btn)
        time.sleep(3 + random.randint(1, 4))

    def process(self):
        if not self.validate():
            raise self.make_step_failed('Invalid params')

        try:
            self.add_card()
            self.add_address()
            self.post_add_address()
            log.warn('Succeed to bind card %s to %s.' % (
                self.card_info.get('card_number'),
                self.account['email']
            ))
        except Exception as ex:
            log.exception('')
            raise StepFailed('Failed to bind_card, due to %s' % ex)
