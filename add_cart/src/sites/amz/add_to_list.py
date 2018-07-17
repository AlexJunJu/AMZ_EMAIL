from __future__ import absolute_import

import time
from .amz_base import AmzBase
from selenium.webdriver.common.by import By


class AddToList(AmzBase):
    _id_add_wishlist_button = (By.ID, 'add-to-wishlist-button-submit')
    _id_view_list = (By.ID, 'WLHUC_viewlist')
    _id_new_list = (By.ID, 'WLNEW_newwl_section')
    _id_submit = (By.ID, 'WLNEW_submit')
    _xpath_view_list = (
        By.XPATH,
        "//*[@class='w-button.w-spacing-top-base']" +
        "//a[contains(@href, 'ref=cm_wl_create_view')]")

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)
        self._is_done = False

    def navigate(self):
        return True

    def post_process(self):
        STATE_INIT = -1
        STATE_NEW = 1
        STATE_VIEW_LIST = 2
        STATE_VIEW_LIST_2 = 3
        STATE_DONE = 4
        STATE_TIMEOUT = 5
        self.state = STATE_INIT

        def _check():
            if self.is_visible(self._id_new_list):
                self.state = STATE_NEW
                return True

            if self.is_visible(self._xpath_view_list):
                self.state = STATE_VIEW_LIST
                return True

            if self.is_visible(self._id_view_list):
                self.state = STATE_VIEW_LIST_2
                return True

            return False

        def _do():
            if self.state == STATE_NEW:
                self.click(self._id_new_list)
                time.sleep(1)
                self.click(self._id_submit)
                self.state = STATE_VIEW_LIST
                return

            if self.state == STATE_VIEW_LIST:
                self.click(self._xpath_view_list)
                self.state = STATE_DONE
                time.sleep(1)
                return

            if self.state == STATE_VIEW_LIST_2:
                self.click(self._id_view_list)
                self.state = STATE_DONE
                time.sleep(1)
                return

        def _timeout():
            self.state = STATE_TIMEOUT

        while self.state not in [STATE_DONE, STATE_TIMEOUT]:
            self.check_and_do(60, _check, _do, _timeout)

    def process(self):
        def _check():
            return self.is_visible(self._id_add_wishlist_button)

        def _do():
            self.click(self._id_add_wishlist_button)
            self._is_done = True
            self.post_process()

	self.check_and_do(60, _check, _do)

    def is_done(self):
        return self._is_done
