from __future__ import absolute_import

import logging as log
import time
import random
from selenium.webdriver.common.by import By
from sites.exception import StepFailed
from .amz_base import AmzBase
from sites.amz.place_order import AbstractPlaceOrderForm
from utils import get_balance


class BaseGiftCard(AmzBase):
    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.market_place_id = params.get('market_place_id')

    def is_euro(self):
        return self.market_place_id in [4, 5, 35691, 44551]

    def validate(self):
        return True

    def navigate(self):
        if not self.validate():
            raise self.make_step_failed('Invalid params')

        # goto account dashboard
        account_link = self.find_alternative_elem(self._nav_link_your_account)
        self.click_elem(account_link, wait_time=5)

        # goto payment
        self.click((By.XPATH, '//div[@data-card-identifier="GiftCards"]'),
                   wait_time=5)

        time.sleep(3 + random.randint(1, 4))

        return True

    def process(self):
        pass


class CheckGiftCard(BaseGiftCard):
    def __init__(self, driver, params, account):
        BaseGiftCard.__init__(self, driver, params, account)

        price_str = str(self.params.get('actual_price', 0.0))
        self.price = get_balance(price_str)
        if '.' not in price_str:
            self.price = self.price * 100

        self.balance = 0

    def get_balance(self):
        # get the current balance
        _balance_elem = (By.XPATH, '//td[@class="gcBalance"]')
        if not self.is_visible(_balance_elem, wait_time=3):
            return False

        balance_elem = self.wait_visible_element(_balance_elem)
        self.balance = get_balance(balance_elem.text)

    def is_enough(self):
        if self.balance == 0:
            self.get_balance()

        return self.balance >= self.price

    def process(self):
        self.get_balance()

        log.warn('Balance %s, need price %s.' % (self.balance, self.price))


class RedeemGiftCard(BaseGiftCard):
    def __init__(self, driver, params, account):
        BaseGiftCard.__init__(self, driver, params, account)
        self.gift_card = self.params.get('gift_card')
        self.balance = 0

    def get_balance(self):
        # get the current balance
        _balance_elem = [(By.XPATH, '//td[@class="gcBalance"]'),
                         (By.ID, 'gc-current-balance')]
        balance_elem = self.find_alternative_elem(_balance_elem)
        if not self.is_valid_elem(balance_elem):
            return False

        self.balance = get_balance(balance_elem.text)

    def navigate(self):
        if not self.gift_card or not self.gift_card['gift_card']:
            return False

        return BaseGiftCard.navigate(self)

    def process(self):
        self.get_balance()
        old_balance = self.balance

        _goto_redeem = (By.XPATH, '//a[contains(@href, "/gp/css/gc/payment")]')
        goto_redeem = self.find_element(*_goto_redeem)
        if goto_redeem:
            self.click_elem(goto_redeem)
            time.sleep(3 + random.randint(1, 3))

        _input_gc = [(By.ID, 'gc-redemption-input'),
                     (By.NAME, 'claimCode')]
        input_gc = self.find_alternative_elem(_input_gc)
        if not input_gc:
            raise self.make_step_failed('Failed to input gift card')
        self.send_keys_to_elem(input_gc, self.gift_card['gift_card'])

        _btn_redeem = [(By.ID, 'gc-redemption-apply-button'),
                       (By.NAME, 'applytoaccount')]
        btn_redeem = self.find_alternative_elem(_btn_redeem)
        if not btn_redeem:
            raise self.make_step_failed('Failed to input gift card')
        self.click_elem(btn_redeem)

        time.sleep(3 + random.randint(1, 3))
        self.get_balance()

        log.warn('old balance %s, new balance is %s.' % (
            old_balance, self.balance))


class BuyGiftCard(BaseGiftCard):

    def __init__(self, driver, params, account):
        BaseGiftCard.__init__(self, driver, params, account)
        self.gift_card = self.params.get('gift_card')
        self.place_order = AbstractPlaceOrderForm(driver, params, account)

    def validate(self):
        if not self.gift_card or not self.gift_card.get('top_up_amount')\
                or int(self.gift_card.get('top_up_amount')) <= 0:
            return False

        return True
        # @TODO Need to check more in future

    def get_formatted_amount(self):
        if not self.validate():
            raise self.make_step_failed('Invalid params')

        amount = self.gift_card.get('top_up_amount') * 100
        amount_text = str(amount/100.0)
        return amount_text if not self.is_euro() \
            else amount_text.replace('.', ',')

    def top_up(self):
        _goto_top_up = (By.XPATH, '//a[contains(@href, "/gp/gc/create")]')
        goto_top_up = self.find_element(*_goto_top_up)
        if goto_top_up:
            self.click_elem(goto_top_up)

        _input_amount = [(By.ID, 'gc-asv-manual-reload-amount'),
                         (By.ID, 'asv-manual-reload-amount'),
                         (By.NAME, 'amount'),
                         (By.NAME, 'manualReload.amount')]
        input_amount = self.find_alternative_elem(_input_amount)
        if not input_amount:
            raise self.make_step_failed('Cannot input top-up amount')

        self.send_keys_to_elem(input_amount, self.get_formatted_amount())

        # some time we will have to confirm the credit card in the same page
        _select_card = (By.NAME, 'instrumentRowSelection')
        if self.is_visible(*_select_card):
            self.click(*_select_card)

            # card_number
            _card_number = [(By.ID, 'addCreditCardNumber'),
                            (By.NAME, 'addCardNumber')]
            card_number = self.find_alternative_elem(_card_number)
            if card_number:
                self.send_keys(_card_number, self.card_info.get('card_number'))

            # confirm card
            _confirm_card = [(By.ID, 'confirm-card'),
                             (By.ID, 'pmts-id-33-announce')]
            confirm_card = self.find_alternative_elem(_confirm_card)
            if confirm_card:
                self.click_elem(confirm_card)
                time.sleep(5 + random.randint(1, 4))

        _check_out = (By.ID, 'form-submit-button')
        self.click(_check_out)
        time.sleep(3 + random.randint(1, 4))

        # purchase the gift card
        self.place_order.paymentment_step()
        self.place_order.review_step()

    def process(self):
        if not self.validate():
            raise self.make_step_failed('Invalid params')

        try:
            self.top_up()
            log.warn('Succeed to buy gift card %s to %s.' % (
                self.gift_card.get('top_up_amount'),
                self.account['email']
            ))
        except Exception as ex:
            log.exception('')
            raise StepFailed('Failed to bind_card, due to %s' % ex)
