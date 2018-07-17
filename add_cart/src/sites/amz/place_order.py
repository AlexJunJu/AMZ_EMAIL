from __future__ import absolute_import

import time
import logging as log
from random import randint
from selenium.webdriver.common.by import By
from .amz_base import AmzBase
from sites.exception import StepFailed
from sites.amz.add_addr import AddOrderAddress
# from utils import get_balance


class BasePlaceOrder(AmzBase):
    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)

        self.asin = params.get('asin')
        self.market_place_id = params['market_place_id']
        self.gc_promo_codes = params.get('gift_cards', [])
        if 'promotion_list' in params:
            self.gc_promo_codes += params['promotion_list']

        self.email = account.get('email')
        self.card_info = self.params.get('credit_card_info', {})

    def navigate(self):
        return True


class AbstractPlaceOrderForm(BasePlaceOrder):

    _order_address_form_gc_promo = [(By.ID, 'gcpromoinput'),
                                    (By.ID, 'spc-gcpromoinput')]
    _order_address_form_apply_gc_promo = [(By.ID, 'button-add-gcpromo'),
                                          (By.ID, 'gcApplyButtonId')]
    _order_address_form_already_redeem = (By.ID, 'addPromo_AlreadyRedeemed')
    _order_address_form_wrong_gc_promo = (By.CSS_SELECTOR, '#gcpromoerrorblock')

    def __init__(self, driver, params, account):
        BasePlaceOrder.__init__(self, driver, params, account)

    def shipment_step(self):
        raise StepFailed('Need to implemented')

    def _use_credict_card(self):
        # We shall keep only one credit card per user in order to simplify the
        # payment case.

        # choose the credit_card
        _card_name = (By.ID, 'credit-card-name')
        if self.is_visible(_card_name, wait_time=2 + randint(1, 4)):
            self.click(_card_name)

        # card_number
        _card_number = [(By.ID, 'addCreditCardNumber'),
                        (By.NAME, 'addCardNumber')]
        card_number = self.find_alternative_elem(_card_number)
        if self.is_valid_elem(card_number):
            self.send_keys_to_elem(card_number,
                                   self.card_info.get('card_number'))

        # confirm card
        _confirm_card = [(By.ID, 'confirm-card'),
                         (By.ID, 'pmts-id-33-announce')]
        confirm_card = self.find_alternative_elem(_confirm_card)
        if confirm_card:
            self.click_elem(confirm_card)
            time.sleep(5 + randint(1, 4))

        # show currencies
        _show_currencies = \
            [(By.XPATH, '//label[contains(@for, "cardOtherCurrency")]'),
             (By.XPATH, '//input[contains(@id, "cardOtherCurrency")]'),
             (By.XPATH,
              '//*[@id="existing-credit-cards-box"]/div[3]/div[2]' +
              '/div[1]/div[1]/div[1]/a')]
        show_currencies = self.find_alternative_elem(_show_currencies)
        if self.is_valid_elem(show_currencies):
            self.click_elem(show_currencies)

        # choose the other currency
        currency_code = self.card_info.get('currency')
        _choose_other_currency = \
            [(By.XPATH, '//input[contains(@name, "cardCurrencyRadio") ' +
              ' and @value="Other"]'),
             (By.XPATH,
              '//*[@id="existing-credit-cards-box"]/div[3]/div[2]' +
              '/div[1]/div[1]/div[2]/label[2]')]
        choose_other_currency = self.find_alternative_elem(
            _choose_other_currency)
        if self.is_valid_elem(choose_other_currency):
            self.click_elem(choose_other_currency, wait_time=1)

        # select the currency
        _currency_btn = (By.XPATH,
                         '//*[@id="existing-credit-cards-box"]/div[3]/' +
                         'div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/' +
                         'span/span/span/button')
        if self.is_visible(_currency_btn, wait_time=3):
            self.click(_currency_btn, wait_time=2)
            time.sleep(3 + randint(1, 4))

            _currencies = (By.XPATH,
                           '//*[@id="1_dropdown_combobox"]/li[*]/a')
            currencies = self.find_elements(*_currencies)
            for currency_elem in currencies:
                data_value = currency_elem.get_attribute('data-value')
                if data_value != currency_code:
                    continue
                self.click_elem(currency_elem, wait_time=2)
                time.sleep(1 + randint(1, 4))
                break
        else:
            _currency_drop_down = (By.ID, 'cardCurrencyDropDown')
            self.select_by_value(_currency_drop_down, currency_code)

    def _apply_gc_promotion(self):
        for gc_promo_code in self.gc_promo_codes:
            if not gc_promo_code.strip():
                continue

            gc_promo = self.find_alternative_elem(
                self._order_address_form_gc_promo)
            if not gc_promo:
                raise self.make_step_failed('Failed to input gc_promo')

            if not gc_promo.is_displayed():
                _address_gc_link = (By.CSS_SELECTOR, '#gc-link-expander')
                self.click(_address_gc_link)

            self.send_keys_to_elem(gc_promo, gc_promo_code)
            time.sleep(1 + randint(1, 4))

            gc_promo_apply = self.find_alternative_elem(
                self._order_address_form_apply_gc_promo)
            if not gc_promo_apply:
                raise self.make_step_failed('Failed to apply gc_promo')
            self.click_elem(gc_promo_apply)
            time.sleep(4 + randint(1, 4))

            if self.is_visible(self._order_address_form_already_redeem):
                continue

            # if self.is_visible(self._order_address_form_wrong_gc_promo):
            #     raise StepFailed('Wrong gc/promo code %s for %s, %s, %s' %
            #                      (gc_promo_code, self.market_place_id,
            #                       self.asin, self.email))

    def get_actual_price(self):
        price_str = ''
        _purchase_total = (By.NAME, 'remainingBalanceRaw')
        purchase_total = self.find_element(*_purchase_total)
        if not purchase_total:
            log.info('price_str %s, 2' % self.params.get('actual_price'))
            return self.params.get('actual_price', 0.0) * 100

        price_str = purchase_total.get_attribute('value')
        log.info('price_str %s, 1' % price_str)
        price_str = price_str.replace(',', '.')
        return float(price_str) * 100

    def get_balance(self):
        balance_str = ''
        _balance_total = (By.NAME, 'gcBalanceRaw')
        balance_total = self.find_element(*_balance_total)
        if balance_total:
            balance_str = balance_total.get_attribute('value')
            if balance_str:
                return float(balance_str) * 100

        return self.params.get('balance', 0.0)

    def paymentment_step(self):
        self._apply_gc_promotion()

        actual_price = self.get_actual_price()
        balance = self.get_balance()
        log.info('actual price %s, balance %s' % (actual_price, balance))
        self.params['remaining_balance'] = \
            (balance - actual_price) if balance >= actual_price else 0

        # Looks like it is a common process
        _place_your_order = (By.NAME, 'placeYourOrder1')
        place_your_order = self.find_element(*_place_your_order)
        if place_your_order:
            return

        # is balance is enough, then use balance directly
        if balance >= actual_price:
            _choose_gc = (By.ID, 'pm_gc_radio')
            if self.is_visible(_choose_gc):
                self.click(_choose_gc)
        else:
            self._use_credict_card()

        # continue to order review page
        _payment_continue = [(By.ID, 'orderSummaryPrimaryActionBtn'),
                             (By.ID, 'continue-top')]
        payment_continue = self.find_alternative_elem(_payment_continue)
        self.click_elem(payment_continue, wait_time=5)
        # still in shipping_payment step
        time.sleep(3 + randint(1, 4))

        _decline_prime = (By.ID, 'prime-pip-updp-decline')
        if self.is_visible(_decline_prime):
            self.click(_decline_prime)
            time.sleep(3 + randint(1, 4))

        _banner = (By.XPATH, '//img[@data-testid="Banner_shippingAndPayment"]')
        if self.is_visible(_banner):
            _submit = (By.XPATH,
                       '//*[@id="piv-popover-container"]/div[3]/div[2]/button')
            self.click(_submit)
            time.sleep(3 + randint(1, 4))

    def review_step(self):
        _place_your_order = [(By.NAME, 'placeYourOrder1'),
                             (By.CSS_SELECTOR, '#submitOrderButtonId')]
        place_your_order = self.find_alternative_elem(_place_your_order)
        if not place_your_order:
            raise self.make_step_failed('Failed to visit "review your order"')

        self.click_elem(place_your_order, wait_time=10)
        time.sleep(5 + randint(1, 9))

    def process(self):
        self.shipment_step()
        self.paymentment_step()
        self.review_step()


class AddressListFormPage(AbstractPlaceOrderForm):
    # inside address-list form
    _order_address_form = (By.CSS_SELECTOR, '#address-list')
    _order_address_form_action = (By.CSS_SELECTOR,
                                  '#orderSummaryPrimaryActionBtn')

    _order_address_form_apply_payment = (By.CSS_SELECTOR,
                                         '#useThisPaymentMethodButtonId')
    _order_address_form_submit = (By.CSS_SELECTOR, '#submitOrderButtonId')

    _new_address = (By.ID, 'add-new-address-popover-link')

    def __init__(self, driver, params, account):
        AbstractPlaceOrderForm.__init__(self, driver, params, account)
        self.add_addr = AddOrderAddress(driver, params, account)

    def shipment_step(self):
        # add new address
        new_address_link = self.find_element(*self._new_address)
        if new_address_link:
            self.click(self._new_address)
            self.add_addr.process()
            time.sleep(3 + randint(1, 4))

        # shipment
        if self.is_valid(self._order_address_form_action, wait_time=3):
            try:
                self.click(self._order_address_form_action)
                time.sleep(4 + randint(1, 4))
            except Exception:
                self.click(self._order_address_form_action)
                time.sleep(4 + randint(1, 4))

        # delivery
        # XXX: it looks that default option is the free delivery
        if self.is_valid(self._order_address_form_action):
            self.click(self._order_address_form_action)
            time.sleep(1 + randint(1, 4))

    def paymentment_step(self):
        AbstractPlaceOrderForm.paymentment_step(self)
        time.sleep(1 + randint(1, 4))

    def review_step(self):
        AbstractPlaceOrderForm.review_step(self)


class AddressDivPage(AbstractPlaceOrderForm):
    # inside address-book-entry-0 div
    _order_div_address = (By.CSS_SELECTOR, '#address-book-entry-0')
    _order_div_address_shipment = \
        (By.CSS_SELECTOR,
         '#address-book-entry-0 > div.ship-to-this-address.' +
         'a-button.a-button-primary.a-button-span12.a-spacing-medium > span')
    _order_div_address_continue = (By.CSS_SELECTOR,
                                   '#shippingOptionFormId > ' +
                                   'div.a-row.a-spacing-medium > ' +
                                   'div.save-sosp-button-box.a-column.' +
                                   'a-span4.a-span-last.a-box.' +
                                   'a-color-alternate-background.' +
                                   'a-right > div > span.' +
                                   'sosp-continue-button.a-button.' +
                                   'a-button-primary.a-button-span12.' +
                                   'a-padding-none.continue-button')
    _order_div_address_continue_eu = (By.NAME, 'continue-bottom')
    # payment page with clear code
    _order_div_address_gc_link = (By.CSS_SELECTOR, '#gc-link-expander')
    _order_div_address_gc_promo = (By.CSS_SELECTOR, '#gcpromoinput')
    _order_div_address_apply_gc_promo = (By.CSS_SELECTOR,
                                         '#button-add-gcpromo')
    _order_div_address_wrong_gc_promo = (By.CSS_SELECTOR, '#gcpromoerrorblock')
    _order_div_address_payment_continue = (By.CSS_SELECTOR, '#continue-top')

    # payment page with encrypted code
    _order_div_address_encrypted_gc_link = (
        By.CSS_SELECTOR,
        '[class="a-expander-header a-declarative a-expander-inline-header ' +
        'pmts-apply-claim-code a-spacing-none a-link-expander"]')
    _order_div_address_encrypted_gc_promo = (
        By.CSS_SELECTOR,
        '[class="a-input-text a-form-normal a-width-medium pmts-claim-code"]')
    _order_div_address_encrypted_apply_gc_promo = (
        By.CSS_SELECTOR,
        '[class="a-button pmts-claim-code-apply-button pmts-button-input"]')
    _order_div_address_encrypted_wrong_gc_promo = (
        By.CSS_SELECTOR, '[class="a-box a-alert a-alert-error"]')
    _order_div_address_encrypted_payment_continue = (
        By.CSS_SELECTOR,
        '[class="a-button a-button-span12 a-button-primary ' +
        'pmts-button-input"]')
    # payment page css selector map
    _order_div_address_payment_page = {
        'clear_page': {
            'gc_link': _order_div_address_gc_link,
            'gc_promo': _order_div_address_gc_promo,
            'apply_gc_promo': _order_div_address_apply_gc_promo,
            'wrong_gc_promo': _order_div_address_wrong_gc_promo,
            'payment_continue': _order_div_address_payment_continue},
        'encrypted_page': {
            'gc_link': _order_div_address_encrypted_gc_link,
            'gc_promo': _order_div_address_encrypted_gc_promo,
            'apply_gc_promo': _order_div_address_encrypted_apply_gc_promo,
            'wrong_gc_promo': _order_div_address_encrypted_wrong_gc_promo,
            'payment_continue': _order_div_address_encrypted_payment_continue}
    }
    _order_div_address_place_order = (By.NAME, 'placeYourOrder1')

    def __init__(self, driver, params, account):
        AbstractPlaceOrderForm.__init__(self, driver, params, account)

    def shipment_step(self):
        # Select a shipping address
        self.click(self._order_div_address_shipment)
        time.sleep(1 + randint(1, 4))

        # Choose your shipping options
        continue_ = None
        if self.is_visible(self._order_div_address_continue):
            continue_ = self._order_div_address_continue
        elif self.is_visible(self._order_div_address_continue_eu):
            continue_ = self._order_div_address_continue_eu
        else:
            raise StepFailed('Unexpected error, ' +
                             'failed to find continue button in shipment_step')

        self.click(continue_)
        time.sleep(1 + randint(1, 4))

    def paymentment_step(self):
        def _common_paymentment_step(css_selector_map):
            # fill in with gift card/promotion code
            for gc_promo_code in self.gc_promo_codes:
                # expand and show gift card/promotion code
                self.click(css_selector_map['gc_link'])
                time.sleep(1 + randint(1, 4))

                gc_promo = self.wait_valid_element(
                    css_selector_map['gc_promo'], wait_time=10)
                gc_promo.clear()
                gc_promo.send_keys(gc_promo_code)
                time.sleep(1 + randint(1, 4))

                self.click(css_selector_map['apply_gc_promo'])
                time.sleep(1 + randint(1, 4))

                # @TODO - make it common
                _order_address_form_already_redeem = \
                    (By.CSS_SELECTOR, '#addPromo_AlreadyRedeemed')
                if self.is_visible(_order_address_form_already_redeem):
                    continue

                # if self.is_visible(css_selector_map['wrong_gc_promo']):
                #     raise StepFailed('Wrong gc_promo_code %s for %s, %s, %s' %
                #                      (gc_promo_code, self.market_place_id,
                #                       self.asin, self.email))

            self.click(css_selector_map['payment_continue'])

        if self.is_visible(self._order_div_address_gc_link):
            return _common_paymentment_step(
                self._order_div_address_payment_page['clear_page'])
        if self.is_visible(self._order_div_address_encrypted_gc_link):
            return _common_paymentment_step(
                self._order_div_address_payment_page['encrypted_page'])

        raise StepFailed('Meet unknown payment page')

    def review_step(self):
        AbstractPlaceOrderForm.review_step(self)


class OrderForNewAddress(AbstractPlaceOrderForm):

    def __init__(self, driver, params, account):
        AbstractPlaceOrderForm.__init__(self, driver, params, account)
        self.add_addr = AddOrderAddress(driver, params, account)

    def shipment_step(self):
        # fill in address
        self.add_addr.process()

        # choose delivery option
        _address_continue = [
            (By.XPATH,
             '//*[@id="shippingOptionFormId"]/div[1]/div[2]/div/span[1]'),
            (By.XPATH,
             '//*[@id="shippingOptionFormId"]/div[3]/div/div/span[1]')]

        address_continue = self.find_alternative_elem(_address_continue)
        if address_continue:
            self.click_elem(address_continue, wait_time=5)

    def paymentment_step(self):
        AbstractPlaceOrderForm.paymentment_step(self)

    def review_step(self):
        AbstractPlaceOrderForm.review_step(self)


class PlaceOrder(AmzBase):
    _order_div_address = (By.CSS_SELECTOR, '#address-book-entry-0')
    _order_address_form = (By.CSS_SELECTOR, '#address-list')
    _ship_to_this_address = (By.NAME, 'shipToThisAddress')

    # inside order placed page
    _order_placed_span = (By.TAG_NAME, 'span')
    _order_no_prefix = 'order-number-'

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.order_no = ''
        self.asin = '|'.join(params.get('asin_list'))
        self.keywords = '|'.join(params.get('kw_list'))
        self.market_place_id = params['market_place_id']
        self.email = account.get('email')
        self._params = params
        self._account = account

    def navigate(self):
        return True

    def get_order_number(self):
        _order_number = (By.XPATH,
                         '//span[contains(@id, "%s")]' % self._order_no_prefix)
        order_number = self.wait_visible_element(_order_number)
        value = order_number.get_attribute('id')
        return value[len(self._order_no_prefix):]

    def click_addr_change(self):
        _addr_change = (By.ID, 'addressChangeLinkId')
        if self.is_visible(_addr_change):
            self.click(_addr_change)
            time.sleep(3 + randint(1, 4))
            return

        _addr_change1 = (By.XPATH,
                         '//*[@id="spc-top"]/div/div[1]/div[1]/div[1]/span')
        if self.is_visible(_addr_change1):
            self.click(_addr_change1)
            time.sleep(3 + randint(1, 4))
            _add_addr = (By.CLASS_NAME, 'add-address-button')
            add_addr_list = self.find_elements(*_add_addr)
            for add_addr in add_addr_list:
                if not add_addr.is_displayed():
                    continue
                self.click_elem(add_addr)
                time.sleep(3 + randint(1, 4))

    def process(self):
        def _get_do_checkout():
            if self.find_elements(*self._ship_to_this_address):
                return OrderForNewAddress(self.driver, self._params,
                                          self._account)
            elif self.find_element(*self._order_address_form):
                return AddressListFormPage(self.driver, self._params,
                                           self._account)
            elif self.find_element(*self._order_div_address):
                return AddressDivPage(self.driver, self._params, self._account)
            else:
                raise StepFailed('Unexpected error')

        def _check_checkout_page():
            return self.find_element(*self._ship_to_this_address) or\
                self.find_element(*self._order_address_form) or\
                self.find_element(*self._order_div_address)

        def _dummy_process():
            pass

        def _timeout_check_checkout_page():
            raise self.make_timeout(
                'Failed to load checkout page. %s, %s, %s' % (
                    self.market_place_id, self.asin, self.email))

        # sometimes we will go to this page firstly
        _banner = (By.XPATH, '//img[@data-testid="Banner_shippingAndPayment"]')
        if self.is_visible(_banner):
            _submit = (By.XPATH,
                       '//*[@id="piv-popover-container"]/div[3]/div[2]/button')
            self.click(_submit)
            time.sleep(3 + randint(1, 4))

        # sometimes amz will try to reuse some old address, so we need to
        # add a new address
        self.click_addr_change()

        self.check_and_do(60, _check_checkout_page, _dummy_process,
                          _timeout_check_checkout_page)

        checkout_page = _get_do_checkout()
        checkout_page.process()

        self.order_no = self.get_order_number()
        asin_list = self.params['asin_list']
        kw_list = self.params['kw_list']
        remaining_balance = checkout_page.params.get('remaining_balance', '-1')
        for i in xrange(len(asin_list)):
            log.warn('Order is placed, %s, %s, %s, %s, %s, %s' % (
                     self.market_place_id, asin_list[i], self.order_no,
                     self.email, kw_list[i], remaining_balance))
