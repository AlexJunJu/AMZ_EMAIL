from __future__ import absolute_import

from random import randint
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .amz_base import AmzBase


class AddAddress(AmzBase):
    url_tmpl = 'https://{market}/gp/css/account/address/view.html' +\
        '?ie=UTF8&ref_=ya_add_address&viewID=newAddress'

    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]
    _address = [
        (By.XPATH, '//div[@data-card-identifier="Addresses"]'),
        (By.XPATH, '//div[@data-card-identifier="AddressesAnd1Click"]')]
    _acct_orders = (By.ID, 'your-orders-button-announce')

    _addr_country_code = [
        (By.ID, 'enterAddressCountryCode'),
        (By.ID, 'address-ui-widgets-countryCode-dropdown-nativeId')]
    _addr_user = [(By.ID, 'enterAddressFullName'),
                  (By.ID, 'address-ui-widgets-enterAddressFullName')]
    _addr_addr1 = [(By.ID, 'enterAddressAddressLine1'),
                   (By.ID, 'address-ui-widgets-enterAddressLine1')]
    _addr_addr2 = [(By.ID, 'enterAddressAddressLine2'),
                   (By.ID, 'address-ui-widgets-enterAddressLine2')]
    _addr_city = [(By.ID, 'enterAddressCity'),
                  (By.ID, 'address-ui-widgets-enterAddressCity')]
    _addr_state = [(By.ID, 'enterAddressStateOrRegion'),
                   (By.ID, 'address-ui-widgets-enterAddressStateOrRegion')]
    _addr_province = [(By.ID,
                       'address-ui-widgets-enterAddressStateOrRegion' +
                       '-dropdown-nativeId')]
    _addr_zip = [(By.ID, 'enterAddressPostalCode'),
                 (By.ID, 'address-ui-widgets-enterAddressPostalCode')]
    _addr_phone = [(By.ID, 'enterAddressPhoneNumber'),
                   (By.ID, 'address-ui-widgets-enterAddressPhoneNumber')]
    _addr_addr_type = [(By.ID, 'AddressType')]
    _addr_gate_code = [(By.ID, 'GateCode'),
                       (By.ID, 'address-ui-widgets-addr-details-gate-code')]

    _addr_submit_btn = [(By.NAME, 'shipToThisAddress'),
                        (By.ID, 'myab_newAddressButton'),
                        (By.XPATH,
                         '//*[@id="address-ui-widgets' +
                         '-enterAddressFormContainer"]/span/span'),
                        (By.XPATH,
                         '//span[@data-action="add-address-popover-submit"]')]

    _addr_suggst_btn = [(By.ID, 'icam_addrSuggestionListSubmitButton'),
                        (By.ID, 'useSelectedAddress'),
                        (By.NAME, 'useSelectedAddress'),
                        (By.NAME,
                         'address-ui-widgets' +
                         '-saveOriginalOrSuggestedAddress')]
    _addr_alert = (By.CLASS_NAME, 'myab-alert-bar-content-text')
    _addr_addr_index_1 = (By.ID, 'addressIndex1')
    _addr_addr_err = (By.CLASS_NAME, 'enterAddressFieldError')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.url = self.url_tmpl.format(**{'market': self.url})
        self.addr_info = self.params.get('addr_info', {})
        self.user_name = '%s %s' % (self.addr_info.get('given_name'),
                                    self.addr_info.get('surname'))

    def validate(self):
        if not self.addr_info:
            return False
        return True

    def navigate(self):
        if not self.validate():
            raise self.make_step_failed('Invalid params')

        # goto account dashboard
        account_link = self.find_alternative_elem(self._nav_link_your_account)
        self.click_elem(account_link, wait_time=5)

        # goto address
        address = self.find_alternative_elem(self._address)
        self.click_elem(address, wait_time=5)

        # goto add address
        self.click((By.ID, 'ya-myab-address-add-link'), wait_time=5)

        return True

    def do_add_address(self):

        def _sendkeys(loc_list, keys, wait_time=3):
            elem = self.find_alternative_elem(loc_list)
            self.send_keys_to_elem(elem, keys, wait_time)

        country_code_elem = self.find_alternative_elem(
            self._addr_country_code)
        country_code = Select(country_code_elem)
        country_code.select_by_value(self.addr_info.get('country_code'))

        _sendkeys(self._addr_user, self.user_name)
        _sendkeys(self._addr_addr1, self.addr_info.get('address_line1'))
        if self.addr_info.get('address_line2'):
            _sendkeys(self._addr_addr2, self.addr_info.get('address_line2'))

        _sendkeys(self._addr_city, self.addr_info.get('city'))

        if self.addr_info.get('state'):
            province_elem = self.find_alternative_elem(self._addr_province)
            if province_elem:
                province = Select(province_elem)
                province.select_by_value(self.addr_info.get('state'))
            else:
                _sendkeys(self._addr_state, self.addr_info.get('state'))

        _sendkeys(self._addr_zip, self.addr_info.get('zip_code'))

        telephone = self.addr_info.get('telephone')
        if not telephone:
            telephone = self.account.get('telephone')

        _sendkeys(self._addr_phone, telephone)

        addr_type_elem = self.find_alternative_elem(self._addr_addr_type)
        if addr_type_elem:
            addr_type = Select(addr_type_elem)
            addr_type.select_by_value('RES' if randint(0, 2) <= 1
                                      else 'COM')
        gate_code = self.find_alternative_elem(self._addr_gate_code)
        if gate_code:
            self.send_keys_to_elem(gate_code, '#%s' % randint(1, 9999))

        submit_btn = self.find_alternative_elem(self._addr_submit_btn)
        self.click_elem(submit_btn)

        time.sleep(3 + randint(1, 4))

    def post_add_address(self):
        addr_suggst_btn = self.find_alternative_elem(self._addr_suggst_btn)
        if addr_suggst_btn:
            self.click_elem(self._addr_suggst_btn)
            time.sleep(3 + randint(1, 4))

        # check whether the address is added or not
        name_elems = self.find_elements(By.ID, 'address-ui-widgets-FullName')
        if not name_elems:
            raise self.make_step_failed('Failed to add address')

        full_names = [elem.text for elem in name_elems]
        if self.user_name not in full_names:
            raise self.make_step_failed('Failed to add address')

    def process(self):
        self.do_add_address()
        self.post_add_address()


class AddOrderAddress(AddAddress):

    def __init__(self, driver, params, account):
        AddAddress.__init__(self, driver, params, account)

    def navigate(self):
        return True

    def post_add_address(self):
        addr_suggst_btn = self.find_alternative_elem(self._addr_suggst_btn)
        if addr_suggst_btn:
            self.click_elem(addr_suggst_btn)
            time.sleep(3 + randint(1, 4))
