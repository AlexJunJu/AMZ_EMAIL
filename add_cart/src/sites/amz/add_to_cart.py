from __future__ import absolute_import

import time
import logging as log
from .amz_base import AmzBase
from sites.exception import StepFailed
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class AddToCart(AmzBase):
    _asin_variant_color = (By.ID, 'variation_color_name')

    _asin_select_size = (By.ID, 'native_dropdown_selected_size_name')
    _asin_asin = (By.NAME, 'ASIN')
    _asin_asin_id = (By.ID, 'ASIN')
    _asin_offer_listing_id = (By.ID, 'offerListingID')

    _asin_quantity = (By.ID, 'quantity')

    _asin_add_to_cart_elems = [(By.ID, 'add-to-cart-button'),
                               (By.ID, 'bb_atc_button'),
                               (By.NAME, 'submit.addToCart'),
                               (By.NAME, 'submit.add-to-cart')]

    _asin_add_to_list_elems = [(By.ID, 'add-to-wishlist-button-submit'),
                               (By.NAME, 'submit.add-to-registry.wishlist')]

    _asin_close_btns = (By.CSS_SELECTOR, '.a-button-close')
    _asin_checkout_btn = (By.CSS_SELECTOR, '#hlb-ptc-btn-native')

    _asin_all_buying_options = (By.CSS_SELECTOR,
                                '#buybox-see-all-buying-choices-announce')

    def __init__(self, driver, params, need_add_to_cart=False):
        AmzBase.__init__(self, driver, params)
        self.need_add_to_cart = need_add_to_cart
        self.asin = params['asin'].upper()
        self.keywords = params['keywords']
        self.variants = params.get('variants', {})\
            .get(self.asin, {})\
            .get('variants', [])

        # TODO need to handle variant correctly in future
        # self.offer_listing_id = params['offer_listing_id']

    def navigate(self):
        return True

    def is_correct_asin(self):
        _hidden_asin = [(By.ID, 'ASIN'), (By.NAME, 'ASIN')]
        hidden_asin = self.find_alternative_elem(_hidden_asin)
        return hidden_asin and hidden_asin.get_attribute('value') == self.asin

    def choose_variant(self):
        if self.is_correct_asin():
            return

        if self.is_visible(self._asin_variant_color, wait_time=8):
            _colors = (By.XPATH, '//li[starts-with(@id, "color_name")]')
            colors = self.find_elements(*_colors)
            for color in colors:
                if self.asin != color.get_attribute('data-defaultasin'):
                    continue
                color.click()
                time.sleep(5 + randint(1, 4))
                break

        if self.is_correct_asin():
            return

        select_elem = self.find_element(*self._asin_select_size)
        if not select_elem:
            raise self.make_step_failed('Failed to choose variant')

        select_ = Select(select_elem)
        for option in select_.options:
            if option.get_attribute('class') != 'dropdownAvailable':
                continue

            val = option.get_attribute('value')
            select_.select_by_value(val)
            time.sleep(5 + randint(1, 4))
            break

        if self.is_correct_asin():
            return

        raise self.make_step_failed('Failed to choose variant')

    def find_add_to_cart_elem(self):
        return self.find_alternative_elem(self._asin_add_to_cart_elems)

    def _do_add_to_cart(self):
        elem = self.find_add_to_cart_elem()
        if not elem or not elem.is_enabled() or not elem.is_displayed():
            return False

        asin_elem = self.find_element(*self._asin_asin_id)
        if asin_elem.get_attribute('ASIN') != self.asin.upper():
            # self.driver.execute_script(
            #     "arguments[0].setAttribute('value', arguments[1])",
            #     asin_elem, self.asin)
            # offer_listing_id_elem = self.find_element(
            #     *self._asin_offer_listing_id)
            # self.driver.execute_script(
            #     "arguments[0].setAttribute('value', arguments[1])",
            #     offer_listing_id_elem, self.offer_listing_id)

            self.make_step_failed('Variant is unsupported at this time')

        self.select_by_value(self._asin_quantity, '1')
        self.click_elem(elem, wait_time=5)

        return True

    def do_add_cart(self):
        def _check():
            elem = self.find_add_to_cart_elem()
            return (elem and elem.is_enabled() and elem.is_displayed()) or\
                self.find_element(*self._asin_all_buying_options)

        def _do():
            if self.is_visible(self._asin_all_buying_options):
                self.click(self._asin_all_buying_options)
                time.sleep(10)

            # add it to cart
            if self._do_add_to_cart():
                return

            self.make_step_failed(
                'Failed to add asin %s to cart, keywords=%s' %
                (self.asin, self.keywords))

        def _timeout():
            self.make_step_failed(
                'Timeout, failed to add asin %s to cart, keywords=%s' %
                (self.asin, self.keywords))

        self.check_and_do(60, _check, _do, _timeout)

    def post_add_cart(self):
        def _get_checkout():
            return self.find_element(*self._asin_checkout_btn)

        def _get_close_btns():
            btns = self.find_elements(*self._asin_close_btns)
            return btns[0] if len(btns) > 0 else None

        def _check():
            return _get_checkout() or _get_close_btns()

        def _do():
            close_btn = _get_close_btns()
            if close_btn:
                self.click_elem(close_btn)

            if _get_checkout():
                return

        def _timeout():
            self.make_step_failed('Timeout, failed to goto checkout')

        self.check_and_do(30, _check, _do, _timeout)

    def process(self):
        self.choose_variant()

        # simulate reading the listing bullet points, decription or reviews
        time.sleep(3 + randint(1, 3))
        for i in xrange(randint(2, 6)):
            self.page_down()
            time.sleep(3 + randint(2, 6))
        self.page_home()

        if not self.need_add_to_cart:
            return

        AddToCart.do_add_cart(self)
        self.post_add_cart()


class AddToCartWithMerchant(AddToCart):
    _asin_seller = (By.CSS_SELECTOR, '#merchant-info > a:nth-child(1)')
    _asin_more_sellers = (By.CSS_SELECTOR,
                          '#mbc > div:nth-child(7) > div > span > a')
    _asin_more_sellers_checkbox_new = (By.NAME, 'olpCheckbox_new')
    _asin_more_sellers_next_btn = (By.CSS_SELECTOR,
                                   '#olpOfferListColumn > ' +
                                   'div.a-text-center.a-spacing-large > ' +
                                   'ul > li.a-last')
    _asin_more_sellers_seller_div = (By.CSS_SELECTOR,
                                     '[class="a-row a-spacing-mini olpOffer"]')
    _asin_more_sellers_seller_div_fba = (
        By.CSS_SELECTOR, '[class="olpBadgeContainer"]')
    _asin_more_sellers_seller_div_seller_col = (
        By.CSS_SELECTOR, '[class="a-spacing-none olpSellerName"]')
    _asin_more_sellers_add_to_cart = (By.NAME, 'submit.addToCart')

    def __init__(self, driver, params, account):
        AddToCart.__init__(self, driver, params, True)
        self.market_place_id = params['market_place_id']
        self.seller = params.get('merchant_name', '')
        self.email = account.get('email')

    def is_same_seller_with_mfn(self):
        if not self.seller:
            return True

        # is the same seller name
        if not self.is_visible(self._asin_seller):
            return False

        seller_elem = self.wait_visible_element(self._asin_seller)
        if not seller_elem.text or \
           seller_elem.text.lower() != self.seller.lower():
            return False

        # is FBA
        href = seller_elem.get_attribute('href')
        return href and href.find('isAmazonFulfilled=1') == -1

    def do_add_cart(self):
        def _check():
            log.info('self._asin_all_buying_options is %s ' %
                     self.find_element(*self._asin_all_buying_options))
            return self.find_element(*self._asin_seller) or \
                self.find_element(*self._asin_more_sellers) or \
                self.find_element(*self._asin_all_buying_options)

        def _do():
            def _do_add_to_cart_via_more_options():
                if self.is_visible(self._asin_more_sellers):
                    self.click(self._asin_more_sellers)
                else:
                    self.click(self._asin_all_buying_options)
                time.sleep(3 + randint(1, 6))

                if self.is_visible(self._asin_more_sellers_checkbox_new):
                    checkbox = self.wait_valid_element(
                        self._asin_more_sellers_checkbox_new)
                    if not checkbox.is_selected():
                        self.click(self._asin_more_sellers_checkbox_new)
                        time.sleep(3 + randint(1, 6))

                def _get_seller_name(div):
                    seller_name_part = div.find_element(
                        *self._asin_more_sellers_seller_div_seller_col)
                    if not seller_name_part:
                        return ''

                    seller_name = seller_name_part.text
                    if seller_name:
                        return seller_name

                    img = seller_name_part.find_element_by_tag_name('img')
                    if not img:
                        return ''
                    seller_name = img.get_attribute('alt')
                    return seller_name if seller_name else ''

                def _process_page():
                    all_divs = self.find_elements(
                        *self._asin_more_sellers_seller_div)
                    for div in all_divs:
                        seller_name = _get_seller_name(div)
                        if self.seller != seller_name:
                            continue

                        # Try to look for the FBA badge
                        try:
                            if div.find_element(
                                    *self._asin_more_sellers_seller_div_fba):
                                continue
                        except Exception:
                            pass

                    return self._do_add_to_cart()

                def _has_more_page():
                    try:
                        next_btn = self.wait_valid_element(
                            self._asin_more_sellers_next_btn)
                        css_clz = next_btn.get_attribute('class')
                        return css_clz.find('a-disabled') == -1
                    except Exception:
                        return False

                def _next_page():
                    self.click(self._asin_more_sellers_next_btn)
                    time.sleep(3 + randint(1, 6))

                while(True):
                    if _process_page():
                        return True

                    if not _has_more_page():
                        break

                    log.info('go to next page')
                    _next_page()

                raise StepFailed('Seller not found, failed to add to cart, ' +
                                 '%s, %s, %s, %s' % (self.market_place_id,
                                                     self.asin, self.email,
                                                     self.keywords))

            if self.is_same_seller_with_mfn():
                if self._do_add_to_cart():
                    time.sleep(3 + randint(1, 6))
                    return True

            return _do_add_to_cart_via_more_options()

        def _timeout():
            raise StepFailed('Timeout, failed to add to cart, %s, %s, %s, %s' %
                             (self.market_place_id, self.asin, self.email,
                              self.keywords))

        self.check_and_do(150, _check, _do, _timeout)

    def process(self):
        if not self.seller:
            AddToCart.process(self)
            return

        self.choose_variant()
        self.do_add_cart()
        self.post_add_cart()
