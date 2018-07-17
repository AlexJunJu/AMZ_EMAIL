from __future__ import absolute_import

from sites.base import BaseStep
from sites.exception import StepFailed
from model import AmzMarketplace


class AmzBase(BaseStep):

    def __init__(self, driver, params):
        BaseStep.__init__(self, driver, params)

        self.url = params.get('marketplace_url')
        if self.url:
            return

        market_place_id = params.get('market_place_id')
        if not market_place_id:
            raise StepFailed('Missing market_place_id')

        market_place = AmzMarketplace.get(market_place_id)
        if not market_place:
            raise StepFailed('Failed to get the marketplace by %s ' %
                             market_place_id)

        params['marketplace_url'] = market_place.website
        self.url = market_place.website
        self.market_place_id = market_place_id


if __name__ == '__main__':

    def ccccc():
        def _aaa():
            c = 'base'

        def _bbb():
            if c:
                print ('ture',c)
            else:
                print('false',c)
        _aaa()
        _bbb()
    ccccc()
