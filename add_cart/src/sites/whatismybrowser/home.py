from __future__ import absolute_import

import logging as log
from sites.base import BaseStep
from selenium.webdriver.common.by import By


class Home(BaseStep):
    url = 'http://whatismybrowser.com/'
    _browser = (By.CSS_SELECTOR,
                '#holder > article.detection-primary.content-block >' +
                'div > div.string-major')

    def navigate(self):
        BaseStep.navigate(self)
        browser = self.find_element(*self._browser)
        log.info('%s ==> %s' % (self.params.get('proxy', 'direct'),
                                browser.text))
