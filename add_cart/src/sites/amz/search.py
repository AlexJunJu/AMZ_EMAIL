from __future__ import absolute_import

import sys
import logging as log
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from sites.exception import TimeoutException, StepFailed
from model import AmzMarketplace
from .amz_base import AmzBase
from urllib import quote_plus
from utils import get_asin_target_url

reload(sys)
sys.setdefaultencoding('utf8')


class Search(AmzBase):
    _search_bar = (By.XPATH, './/*[@id=\'twotabsearchtextbox\']')
    _search_qid = (By.NAME, 'qid')
    _search_any_category = (By.CLASS_NAME, 'shoppingEngineExpand')
    _search_any_category_1 = (By.CLASS_NAME, 'root')
    _search_dropdown_box = (By.ID, 'searchDropdownBox')
    _search_center_plus = (By.ID, 'centerPlus')

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)
<<<<<<< HEAD
        # no 'keywords'
        self.keywords = params['keywords']
        self.brand = params['brand']
        #para in params not include 'group_desc'
=======
        self.keywords = params['keywords']
        self.brand = params['brand']
>>>>>>> ea1f2b1c1d5258298be1420381d67e8cb003c069
        self.group_desc = params.get('group_desc', 'aps').lower()

    def navigate(self):
        return True

    def process(self):
        def _check():
            return self.find_element(*self._search_bar) is not None

        def _do():
            elem = self.wait_valid_element(self._search_bar)
            elem.clear()
            elem.send_keys(self.keywords)
            elem.send_keys(Keys.ENTER)

        def _timeout():
            raise TimeoutException('Network issue, failed to find search bar')

        self.check_and_do(60, _check, _do, _timeout)

    def get_any_category(self):
        any_category = self.find_element(*self._search_any_category)
        if not any_category:
            any_category = self.find_element(*self._search_any_category_1)
            if not any_category:
                return None

            return any_category.find_element(By.TAG_NAME, 'li')

        return any_category

    def click_any_category(self):
        def _check():
            return self.get_any_category() is not None

        def _do():
            self.click_elem(self.get_any_category())

        self.check_and_do(8, _check, _do)

    def click_group_desc(self):
        def _check():
            return self.find_element(*self._search_dropdown_box) is not None

        def _do():
            search_dropdown_box = self.find_element(*self._search_dropdown_box)
            select = Select(search_dropdown_box)
            select.select_by_value(
                'search-alias=%s' % self.group_desc)
            log.warning('KwRankIMpr: Click keywords: %s, group desc %s'
                        % (self.keywords, self.group_desc))

        self.check_and_do(8, _check, _do)

    def click_center_plus(self):
        def _check():
            center_plus = self.find_element(*self._search_center_plus)
            if not center_plus:
                return False

            center_plus_link = center_plus.find_element_by_class_name(
                'a-link-normal')
            if not center_plus_link:
                return False

            return True

        def _do():
            center_plus = self.find_element(*self._search_center_plus)
            center_plus_link = center_plus.find_element_by_class_name(
                'a-link-normal')
            center_plus_link.click()

        self.check_and_do(8, _check, _do)


class SearchAndGotoAsin(Search):
    def __init__(self, driver, params):
        Search.__init__(self, driver, params)
        self.market_place_id = params['market_place_id']
<<<<<<< HEAD
        self.asin = params['asin']#None
        self.canonical_url = params.get('canonical_url', '')#None
=======
        self.asin = params['asin']
        self.canonical_url = params.get('canonical_url', '')
>>>>>>> ea1f2b1c1d5258298be1420381d67e8cb003c069
        self.variants = params.get('variants', {})\
            .get(self.asin, {})\
            .get('variants', [])

    def get_qid(self):
        qids = self.find_elements(*self._search_qid)
        return qids[0].get_attribute('value') if qids else 'NULL'

    def get_asin_ranking(self):
        return randint(3, 60), False

    def go_to_asin_and_click(self):
        STATE_WRONG = -1
        STATE_DONE = 1
        STATE_LOOK_FOR_1ST_PAGE = 2
        STATE_LOOK_FOR_POS = 3
        STATE_LOOK_FOR_BRAND = 4
        STATE_SURL = 5
        STATE_FOUND = 99

        url_tmpl = 'https://{market}/s/ref=sr_pg_{page}?' + \
            'rh=i%3A{group_desc}%2Ck%3A{keywords}&page={page}' + \
            '&keywords={keywords}&qid={qid}'''

        def _if_asin_in_page(context):
            # asin = context['asin']
            variants = context['variants']
            if context['asin'] not in variants:
                variants.append(context['asin'])

            all_asins_info = self.driver.\
                find_elements_by_class_name('s-result-item')
            all_asins_info = {ai.get_attribute('data-asin'): ai for
                              ai in all_asins_info if
                              not not ai.get_attribute('data-asin')}
            all_asins_info = all_asins_info.values()
            for ai in all_asins_info:
                ai_asin = ai.get_attribute('data-asin')
                if ai_asin in variants and\
                        not ai.find_elements_by_tag_name('h5'):
                    return ai, len(all_asins_info)

            if context['state'] == STATE_LOOK_FOR_BRAND:
                log.warning(('market: %s, brand: %s, keywords: %s, ' +
                            'asin: %s does not exist') %
                            (context['market'], context['brand'],
                             context['keywords'], context['asin']))
            return None, len(all_asins_info)

        def _get_asin_page(item_count):
            ranking, is_rank = self.get_asin_ranking()
            if not is_rank:
                return False

            if item_count == 0:
                item_count = 15
            page = ranking / item_count if ranking % item_count == 0\
                else ranking / item_count + 1

            return page

        def _failure(context):
            sm = context['state_machine']
            state = context['state']
            failure = sm[state]['failure']
            return failure(context) if callable(failure) else failure

        def _check_result(context):
            asin_info, page_item_count = _if_asin_in_page(context)
            context['asin_info'] = asin_info
            context['page_item_count'] = page_item_count

            if not asin_info:
                return _failure(context)

            sm = context['state_machine']
            state = context['state']
            return sm[state]['success']

        def _handle_1st_page(context):
            return _check_result(context)

        def _handle_position_page(context):
            if not context.get('page_item_count', None):
                raise StepFailed('Failed to get the asin info by %s ' %
                                 self.asin)

            page = _get_asin_page(context['page_item_count'])
            if not page:
                return _failure(context)

            url_dict = dict(market=context['market'].website,
                            qid=self.get_qid(),
                            keywords=context['keywords'],
                            page=page, group_desc=self.group_desc)
            self.driver.get(url_tmpl.format(**url_dict))
            return _check_result(context)

        def _handle_brand_page(context):
            if not context['brand']:
                return _failure(context)

            if not context.get('BRAND_NEXT_PAGE'):
                self.click_brand_url()

            return _check_result(context)

        def _get_brand_failure(context):
            _next_page = (By.ID, 'pagnNextLink')
            next_page = self.find_element(*_next_page)
            if not next_page:
                return STATE_SURL

            _next_page_span = (By.ID, 'pagnNextString')
            self.click(_next_page_span)
            context['BRAND_NEXT_PAGE'] = True
            return STATE_LOOK_FOR_BRAND

        def _handle_surl(context):
            self.driver.get(self.make_url(self.get_qid(), context))
            return STATE_DONE

        def _transit(context, state):
            context['state'] = state

        market = AmzMarketplace.get(self.market_place_id)
        if not market:
            raise StepFailed('Failed to get the marketplace by %s ' %
                             self.market_place_id)

        state_machine = {STATE_LOOK_FOR_1ST_PAGE: {'handle': _handle_1st_page,
                                                   'success': STATE_FOUND,
<<<<<<< HEAD
                                                   'failure':STATE_LOOK_FOR_BRAND},
=======
                                                   'failure':
                                                   STATE_LOOK_FOR_BRAND},
>>>>>>> ea1f2b1c1d5258298be1420381d67e8cb003c069
                         STATE_LOOK_FOR_POS: {'handle': _handle_position_page,
                                              'success': STATE_FOUND,
                                              'failure': STATE_LOOK_FOR_BRAND},
                         STATE_LOOK_FOR_BRAND: {'handle':
                                                _handle_brand_page,
                                                'success': STATE_FOUND,
                                                'failure': _get_brand_failure},
                         STATE_SURL: {'handle': _handle_surl,
                                      'success': STATE_DONE,
                                      'failure': STATE_WRONG}}

        context = {'asin': self.asin,
                   'variants': self.variants,
                   'brand': self.brand,
                   'group_desc': self.group_desc,
                   'market': market,
                   'keywords': quote_plus(str(self.keywords)),
                   'state_machine': state_machine,
                   'state': STATE_LOOK_FOR_1ST_PAGE}

        while True:
            sm = context['state_machine'][context['state']]
            state = sm['handle'](context)

            if state == STATE_WRONG:
                return False

            if state == STATE_DONE:
                return True

            if state == STATE_FOUND:
                break

            _transit(context, state)

        asin_detail = context['asin_info'].\
            find_element_by_class_name('s-access-detail-page')
        if asin_detail.get_attribute('target'):
            self.driver.get(asin_detail.get_attribute('href'))
            return True

        asin_detail.click()

        return True

    def make_url(self, qid, context, ranking=None):
        def _get_ref_rank(market, rank, group_desc):
            special_group = {1: ['baby-products', 'beauty', 'hpc', 'grocery'],
                             3: ['beauty', 'drugstore', 'grocery'],
                             4: [], 5: [], 6: [], 7: [], 35691: [],
                             44551: []}
            return '%s%s' % (rank,
                             '_s_it' if group_desc in
                             special_group[market] else '')

        def _get_sr_rank(rank, group_desc):
            return '%s-%s' % (8 if group_desc == 'aps' else 1, rank)

        def _get_group_desc(group_desc):
            return 's=%s&' % group_desc if group_desc != 'aps' else ''

        url_tmpl = 'https://{market}/dp/{asin}/' + \
            'ref=sr_1_{ref_rank}?{group_desc}ie=UTF8&qid={qid}&' + \
            'sr={sr_rank}&keywords={keywords}'

        if not ranking:
            ranking, _ = self.get_asin_ranking()

        market = context['market']
        return url_tmpl.format(**{'market': market.website,
                                  'asin': self.asin,
                                  'rank': ranking,
                                  'ref_rank': _get_ref_rank(market.id,
                                                            ranking,
                                                            self.group_desc),
                                  'group_desc': _get_group_desc(
                                      self.group_desc),
                                  'sr_rank': _get_sr_rank(ranking,
                                                          self.group_desc),
                                  'keywords': context['keywords'],
                                  'qid': qid})

    def click_brand_url(self):
        asin_info = dict(brand=self.brand, group_desc=self.group_desc,
                         market=self.market_place_id,
                         keywords=self.keywords)
        brand_url = get_asin_target_url(url_type=1, asin_data=asin_info)
        self.driver.get(brand_url)
        return True

    def process(self):
        Search.click_group_desc(self)
        Search.process(self)
        # if self.group_desc == 'aps':
        #    Search.click_any_category(self)
        if self.group_desc == 'hpc':
            Search.click_center_plus(self)
        self.go_to_asin_and_click()
