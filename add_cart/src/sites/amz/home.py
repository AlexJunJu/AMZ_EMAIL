from __future__ import absolute_import

from selenium.webdriver.common.by import By
from .amz_base import AmzBase
from sites.exception import TimeoutException


class Home(AmzBase):

    _search_bar = (By.XPATH, './/*[@id=\'twotabsearchtextbox\']')

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)
        self.url = 'http://{market}'.format(**{'market': self.url})

    def is_done(self):
        return self.find_element(*self._search_bar) is not None

    def navigate(self):
        def _check():
            return self.find_element(*self._search_bar)

        def _do():
            pass

        def _timeout():
            raise TimeoutException('Failed to load HOME page')

        self.driver.get(self.url)
        self.check_and_do(30, _check, _do, _timeout)
        return True
