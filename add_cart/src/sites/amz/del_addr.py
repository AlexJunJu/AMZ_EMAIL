
from __future__ import absolute_import

from selenium.webdriver.common.by import By
from sites.exception import TimeoutException, StepFailed
from .amz_base import AmzBase


class DeleteAddress(AmzBase):
    url_tmpl = 'https://{market}/gp/css/account/address/view.html' +\
        '?ie=UTF8&ref_=ya_manage_address_book'

    _nav_link_your_account = (By.ID, 'nav-link-yourAccount')
    _del_first_addr = (By.ID, 'myab_AddrBookDeleteAddr_1')
    _confirm_del_addr = (By.ID, 'icam_deleteAddressButton')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.url = self.url_tmpl.format(**{'market': self.url})

    def has_address(self):
        return self.find_element(*self._del_first_addr)

    def navigate(self):
        def _check():
            return self.find_element(*self._nav_link_your_account)

        def _do():
            self.driver.get(self.url)

        def _timeout():
            raise TimeoutException('Network issue, failed visit address form')

        if not _check():
            raise StepFailed('Cannot visit address form via account home')

        self.check_and_do(60, _check, _do, _timeout)
        return True

    def post_del_address(self):

        def _check():
            return self.find_element(*self._del_first_addr)

        def _do():
            del_btn = self.find_element(*self._del_first_addr)
            del_btn.click()

        def _timeout():
            raise TimeoutException('Network issue, failed to delete addr')

        self.check_and_do(60, _check, _do, _timeout)

    def confirm_delete_address(self):
        def _check():
            return self.find_element(*self._confirm_del_addr)

        def _do():
            confirm_delete_btn = self.find_element(*self._confirm_del_addr)
            confirm_delete_btn.click()

        def _timeout():
            raise TimeoutException('Network issue,' +
                                   'failed to confirm deleteting')

        self.check_and_do(60, _check, _do, _timeout)

    def process(self):
        if self.has_address():
            self.post_del_address()
            self.confirm_delete_address()
