from __future__ import absolute_import

import logging as log
from sites.base import BaseStep
from selenium.webdriver.common.by import By


class Home(BaseStep):
    url = 'http://whatismyipaddress.com/'
    _ip_addr = (By.CSS_SELECTOR, '#section_left > div:nth-child(2) > a')

    def navigate(self):
        BaseStep.navigate(self)
        ipaddr = self.find_element(*self._ip_addr)
        log.info('%s ==> %s' % (self.params.get('proxy', 'direct'),
                                ipaddr.text))
