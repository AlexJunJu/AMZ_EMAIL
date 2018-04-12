from __future__ import absolute_import

import time
import logging as log
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from sites.exception import TimeoutException
from .amz_base import AmzBase
from datetime import datetime


class SetupList(AmzBase):
    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]
    _wish_list_page = (By.ID, 'wishlist-page')
    _your_lists_nav = (By.ID, 'your-lists-nav')
    _list_setting = (By.CLASS_NAME, 'a-fixed-right-grid-col')
    _list_privacy = (
        By.CSS_SELECTOR, '.a-fixed-right-grid-col.wl-list-privacy.a-col-right')
    _manage_form = (By.ID, 'g-manage-form')
    _radio_default = (By.NAME, 'default')
    _submit_btn = (By.NAME, 'submit')
    _default_radio_btn = (By.NAME, 'default')
    _table_wishlist = (By.ID, 'g-manage-table-wishlist')
    _selected_item = (By.CSS_SELECTOR, '.selected')
    _row_name = (By.CLASS_NAME, 'g-manage-name')
    _row_privacy = (By.CLASS_NAME, 'g-manage-privacy')
    _row_delete = (By.CLASS_NAME, 'g-manage-delete')
    _row_default = (By.CLASS_NAME, 'g-manage-default')
    _input_tag = (By.TAG_NAME, 'input')
    _is_private = (By.TAG_NAME, 'select')
    _row_wishlist = (By.TAG_NAME, 'tr')
    _list_item_name = (By.CSS_SELECTOR, "a[id*=wl-list-link]")
    _list_item_privacy = (
        By.CSS_SELECTOR, "[id^=wl-list-privacy] a.a-link-normal.a-declarative")
    _xpath_wish_list = (
        By.XPATH,
        "//*[@class='a-spacing-micro']//a[contains(@href, 'ya_d_l_lists')]")
    _xpath_list_settings = (
        By.XPATH,
        "//a[contains(@href, '/registry/side/manage/ref=cm_wl_mng_lists')]")

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)
        self.setup_done = False
        self.account_name = 'amz' if 'account_name' not in params.keys() else\
            params['account_name']

    def navigate(self):

        def _check():
            self.nav_elem = self.find_alternative_elem(
                self._nav_link_your_account)
            return False if not self.nav_elem else True

        def _process():
            self.click_elem(self.nav_elem)

            def _check():
                return self.is_visible(self._xpath_wish_list, wait_time=10)

            def _do():
                self.click(self._xpath_wish_list)

            self.check_and_do(45, _check, _do)

        def _timeout():
            raise TimeoutException('Network issue, failed to find login')

        self.check_and_do(60, _check, _process, _timeout)
        return True

    def is_done(self):
        return self.setup_done

    def process(self):
        def _check():
            return self.is_visible(self._wish_list_page)

        def _do():
            list_settings = self.find_elements(*self._list_setting)
            if not list_settings:
                return

            list_settings = [ll for ll in list_settings
                             if ll.get_attribute('id').startswith('wl-list')]
            if not list_settings:
                return

            a_elem = list_settings[0].find_element_by_tag_name('a')
            if not a_elem:
                return

            self.click_elem(a_elem)
            time.sleep(1)

            form = self.find_element(*self._manage_form)
            if not form:
                return

            submit_btn = form.find_element_by_name('submit')
            if not submit_btn:
                return

            radio_btns = form.find_elements_by_name('default')
            if not radio_btns:
                self.click_elem(submit_btn)
                return

            radio_btn = radio_btns[randint(0, len(radio_btns) - 1)]
            self.click_elem(radio_btn)
            self.setup_done = True
            self.click_elem(submit_btn)

        def _timeout():
            raise TimeoutException('Network issue, failed to find wish list')

        self.check_and_do(60, _check, _do, _timeout)

    def make_list_name(self):
        return self.account_name + datetime.utcnow().strftime('%Y%m%d%H%M%S')

    def change_setup(self, list_token):
        def _check():
	    return self.is_visible(self._xpath_list_settings)

        def _do():
            def _check():
                return self.is_visible(self._table_wishlist, wait_time=10) and\
                    self.is_visible(self._manage_form, wait_time=10)

            def _process():
                OPTION_PUBLIC = str(0)
                form_wishlist = self.wait_visible_element(self._manage_form)
                table_wishlist = self.find_element(*self._table_wishlist)
                row_wishlist = table_wishlist.find_elements(
                    *self._row_wishlist)
                for row_elem in row_wishlist:
                    try:
                        row_elem.find_element(*self._row_name)
                    except:
                        continue

                    name_elem = row_elem.find_element(*self._row_name)
                    input_elem = name_elem.find_element(*self._input_tag)
                    if not input_elem or list_token \
                            not in input_elem.get_attribute('name'):
                        continue

                    self.name = input_elem.get_attribute('value')
                    if not self.name or\
                            not self.name.startswith(self.account_name):
                        input_elem.clear()
                        self.name = self.make_list_name()
                        input_elem.send_keys(self.name)

                    privacy_elem = row_elem.find_element(*self._row_privacy)
                    privacy_drop_down = privacy_elem.find_element(
                        *self._is_private)
                    if not privacy_drop_down:
                        continue

                    select = Select(privacy_drop_down)
                    options = select.all_selected_options
                    options = select.all_selected_options
                    if not options or OPTION_PUBLIC !=\
                            options[0].get_attribute('value'):
                        select.select_by_value(OPTION_PUBLIC)
                        time.sleep(3)
                    self.privacy = OPTION_PUBLIC
                    break

                submit_btn = form_wishlist.find_element(*self._submit_btn)
                self.click_elem(submit_btn)
                time.sleep(5)
                self.setup_done = True

	    clickable_elem = self.wait_valid_element(
		self._xpath_list_settings,
		wait_time=10)
            self.click_elem(clickable_elem)
	    log.info('click list settings to change setup')
            self.check_and_do(90, _check, _process)

        self.check_and_do(120, _check, _do)

    def change_default(self, list_token):
        def _check():
	    return self.is_visible(self._xpath_list_settings)

        def _do():
            def _check():
                return self.is_visible(self._manage_form)

            def _process():
                form_wishlist = self.find_element(*self._manage_form)
                radio_btns = form_wishlist.find_elements(
                    *self._default_radio_btn)
                for rt in radio_btns:
                    if list_token in rt.get_attribute('value'):
                        self.click_elem(rt)
                        break
                time.sleep(3)
                submit_btn = form_wishlist.find_element(*self._submit_btn)
                self.click_elem(submit_btn)
                time.sleep(5)
                self.setup_done = True

	    clickable_elem = self.wait_valid_element(
		self._xpath_list_settings,
		wait_time=10)
            self.click_elem(clickable_elem)
            self.check_and_do(40, _check, _process)

        def _timeout():
            raise TimeoutException('Network issue, failed to find wish list')

        self.check_and_do(60, _check, _do, _timeout)
