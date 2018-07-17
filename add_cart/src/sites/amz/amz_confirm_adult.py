from __future__ import absolute_import

import logging as log
from model import AmzMarketplace
from .amz_base import AmzBase
from selenium.webdriver.common.by import By


class ConfirmAdult(AmzBase):
    _center = (By.TAG_NAME, 'center')

    def __init__(self, driver, params, asin, canonical_url):
        AmzBase.__init__(self, driver, params)
        self.market_place_id = params['market_place_id']
        self.canonical_url = canonical_url
        self.asin = asin

    def make_url(self):
        url_tmpl = 'https://{market}/{url_name}/dp/{asin}/'
        market = AmzMarketplace.get(self.market_place_id)

        return url_tmpl.format(**{'market': market.website,
                                  'url_name': self.canonical_url,
                                  'asin': self.asin})

    def navigate(self):
        return True

    def process(self):
        # ???self.driver.get()
        self.driver.get(self.make_url())
        # can't find 'center' 'redirectUrl'
        center = self.find_element(*self._center)
        if not center:
            return

        a_elems = center.find_elements_by_tag_name('a')
        for a_elem in a_elems:
            if 'redirectUrl' in a_elem.get_attribute('href'):
                return self.click_elem(a_elem)
