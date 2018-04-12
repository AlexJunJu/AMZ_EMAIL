# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import logging as log
import time
import re
from random import randint
from selenium.webdriver.common.by import By
from sites.exception import TimeoutException, MeetSpammedAccount
from sites.amz.decaptcha import Decaptcha
from .amz_base import AmzBase

reload(sys)
sys.setdefaultencoding('utf8')


class Signin(AmzBase):
    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]
    _search_bar = (By.XPATH, './/*[@id=\'twotabsearchtextbox\']')

    _signin_auth_err = (By.ID, 'auth-error-message-box')
    _signin_email = (By.ID, 'ap_email')
    _sigin_password = (By.ID, 'ap_password')
    _sigin_submit = (By.ID, 'signInSubmit')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.market_place_id = params.get('market_place_id')

    def is_in_signin_page(self):
        return self.is_visible(self._signin_email, wait_time=10)

    def is_done(self):
        return self.find_element(*self._search_bar) is not None

    def is_auth_err(self):
        return self.find_element(*self._signin_auth_err) is not None

    def is_new_account(self):
        auth_err = self.find_element(*self._signin_auth_err)
        err_msg = {
            '1': 'We cannot find an account',
            '3': 'We cannot find an account',
            '4': 'Es konnte kein Konto',
            '5': 'Impossible de trouver un compte correspondant',
            '35691': 'Non riusciamo a trovare un account',
            '44551': 'No encontramos ninguna cuenta',
            '6': 'つアカウントが見つかりません',
            '7': 'We cannot find an account',
        }

        msg = err_msg.get(self.market_place_id, '')
        return msg and msg in auth_err.text

    def navigate(self):

        def _check():
            self.nav_elem = self.find_alternative_elem(
                self._nav_link_your_account)
            return False if not self.nav_elem else True

        def _do():
            self.click_elem(self.nav_elem)

        def _timeout():
            raise TimeoutException('Failed to find signin menu item')

        self.check_and_do(60, _check, _do, _timeout)
        return True

    def click_confirm(self):
        _confirm = [(By.ID, 'dcq_submit'),
                    (By.XPATH,
                     '//*[@id="cvf-page-content"]/div/div/div[1]' +
                     '/form/div[4]/span')]
        confirm = self.find_alternative_elem(_confirm)
        if not confirm:
            raise self.make_step_failed(
                'Failed to login with %s, confirm button not found' %
                self.account.get('email'))
        self.click_elem(confirm)

    def handle_phone_verification(self):
        _telphone_input = (By.ID, 'dcq_question_subjective_1')
        if not self.is_visible(_telphone_input, wait_time=3):
            return True

        _challenge_0 = (By.ID, 'challenge_0')
        ch_text = ''
        if self.is_visible(_challenge_0, wait_time=1):
            challenge_0 = self.find_element(*_challenge_0)
            ch_text = ''.join(re.findall('\d', challenge_0.text))
            telephones = self.account.get('telephones', '')
            if not telephones:
                telephones = self.account.get('telephone')

            phone_list = [phone for phone in telephones.split(',')]
            if ch_text:
                phone_list = [phone for phone in phone_list if ch_text in phone]
            for phone in phone_list:
                self.send_keys(_telphone_input, phone.strip())
                self.click_confirm()

                time.sleep(5 + randint(1, 4))
                if self.is_done():
                    return True
            else:
                return False
        else:
            _question = (By.XPATH, '//label[@for="question"]')
            if not self.is_visible(_question, wait_time=1):
                raise self.make_step_failed(
                    'Failed to find question to verify %s' %
                    self.account.get('email'))
            credit_card_list = self.account.get('credit_card_list')
            question = self.find_element(*_question)
            q_text = ''.join(re.findall('\d', question.text))
            credit_card_list = [cc for cc in credit_card_list
                                if cc.get('card_number', '').endswith(q_text)]
            for cc in credit_card_list:
                self.send_keys(_telphone_input, cc.get('zip_code').strip())
                self.click_confirm()

                time.sleep(5 + randint(1, 4))
                if self.is_done():
                    return True
            else:
                raise self.make_step_failed(
                    'Failed to find credit_card_list to verify %s' %
                    self.account.get('email'))

    def process(self):
        def _check():
            return self.find_element(*self._signin_email)

        def _do():
            email = self.wait_valid_element(self._signin_email)
            password = self.wait_valid_element(self._sigin_password)

            email.clear()
            email.send_keys(self.account.get('email'))
            password.clear()
            password.send_keys(self.account.get('password'))
            self.click(self._sigin_submit)

        self.check_and_do(30, _check, _do)

        # meet "checking code from email"
        _code_input = (By.NAME, 'code')
        if self.is_visible(_code_input, wait_time=3):
            raise self.make_step_failed(
                'Failed to login with %s, need email verification' %
                self.account.get('email'))

        # meet telphone verification
        if not self.handle_phone_verification():
            raise self.make_step_failed(
                'Failed to login with %s, phone number error' %
                self.account.get('email'))

        # meet other verification
        _telphone_input = (By.ID, 'dcq_question_subjective_2')
        if self.is_visible(_telphone_input):
            raise self.make_step_failed(
                'Failed to login with %s, need more verification' %
                self.account.get('email'))

        if not self.is_done():
            raise self.make_step_failed(
                'Failed to login with %s, unknown error' %
                self.account.get('email'))

        log.info('Succeed to login with %s' % self.account.get('email'))


class SigninWithCaptcha(AmzBase):

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.signin = Signin(driver, params, account)
        self.decaptcha = Decaptcha(driver, params, account,
                                   lambda: self.signin.process())

    def is_in_signin_page(self):
        return self.signin.is_in_signin_page()

    def is_done(self, timeout=60):
        def _check():
            return self.signin.is_done() or self.is_auth_err() or\
                self.decaptcha.has_met_captcha()

        return self.check_and_do(timeout, _check, _check, _check)

    def is_auth_err(self):
        return self.signin.is_auth_err()

    def is_new_account(self):
        return self.signin.is_new_account()

    def navigate(self):
        self.signin.navigate()
        return True

    def process(self):
        self.signin.process()
        if self.signin.is_done():
            return

        for i in xrange(0, 6):
            if self.signin.is_auth_err():
                return
            if not self.decaptcha.has_met_captcha():
                log.error('[ERROR]: ' + self.driver.page_source)
                return

            self.decaptcha.process()

        raise MeetSpammedAccount('Failed to decaptcha for %s' %
                                 self.signin.account.get('email'))
