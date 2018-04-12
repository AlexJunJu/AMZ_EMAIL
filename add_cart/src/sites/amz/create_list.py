from __future__ import absolute_import

import logging as log
from .amz_base import AmzBase
from selenium.webdriver.common.by import By
from sites.exception import TimeoutException
from .setup_list import SetupList
import time


class CreateList(AmzBase):

    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]
    _id_nav_wish_list = (By.ID, 'nav-link-wishlist')
    _id_create_list_arr = [(By.ID, 'createList'), (By.ID, 'a-autoid-0')]
    _id_my_list = (By.ID, 'your-lists-nav')
    _selected_item = (By.CSS_SELECTOR, '.selected')
    _pop_over_create_list = (
        By.CSS_SELECTOR, '.a-popover.a-popover-modal.a-declarative.pop-create')
    _id_btn_create_list = (By.ID, 'a-autoid-1')
    _xpath_create_button = (By.XPATH,
                            "//span[@data-action='reg-create-submit']")
    _name_input_create_name = (By.NAME, 'create-name')
    _list_item_name = [(By.CSS_SELECTOR, "a[id*='wl-list-link']"),
                       (By.CSS_SELECTOR, "span[id*='wl-list-title']")]
    _xpath_wish_list = (
        By.XPATH,
        "//*[@class='a-spacing-micro']//a[contains(@href, 'ya_d_l_lists')]")

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)
        self.setup_list = SetupList(driver, params)

    def destroy(self):
        self.list_token = None
        self.name = None
        self.privacy = None
        self.nav_elem = None
        self.create_button = None

    def navigate(self):
        def _check():
            self.nav_elem = self.find_visible_elem(
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

    def change_setup(self):
	def _parse_list_token(parsed_elem):
	    id_str = parsed_elem.get_attribute('id')
	    match = ['wl-list-link-', 'wl-list-title-']
	    for cmp_str in match:
		if id_str.startswith(cmp_str):
		    return id_str[len(cmp_str):]

        def _check():
            return self.is_visible(self._id_my_list, wait_time=10)

        def _process():
            my_list = self.wait_visible_element(self._id_my_list, wait_time=10)
            selected_item = my_list.find_element(*self._selected_item)
            if not selected_item:
                return
	    for elem in self._list_item_name:
		try:
	            selected_elem = selected_item.find_element(*elem)
		except Exception as err:
		    log.info('Normal: NoSuchElementException, check next elem')
		    continue
	        if selected_elem:
		    self.list_token = _parse_list_token(selected_elem)
		    break
	    else:
		log.error('No such element')
		return
            self.setup_list.change_setup(self.list_token)
	    if hasattr(self.setup_list, 'name'):
		self.name = self.setup_list.name
	    if hasattr(self.setup_list, 'privacy'):
                self.privacy = self.setup_list.privacy

        self.check_and_do(60, _check, _process)

    def create_list_by_popover(self):
        def _check():
	    return self.is_visible(self._name_input_create_name)

        def _process():
	    list_name = self.wait_valid_element(
		self._name_input_create_name,
		wait_time=10)
            list_name.clear()
            self.name = self.setup_list.make_list_name()
            list_name.send_keys(self.name)
	    try:
                self.click(self._id_btn_create_list)
	    except Exception as err:
		log.error(err)
		self.click(self._xpath_create_button)
	    log.info('popover: press create button')

        self.check_and_do(45, _check, _process)
        time.sleep(8)

    def process(self):
        def _check():
            self.create_button = self.find_visible_elem(
                self._id_create_list_arr)
            return False if not self.create_button else True

        def _process():
            self.click_elem(self.create_button)
            self.create_list_by_popover()
            self.change_setup()

        def _timeout():
            raise TimeoutException(
                'Network issue, failed to find create_button')

        self.check_and_do(120, _check, _process, _timeout)
