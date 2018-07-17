from __future__ import absolute_import

from selenium.webdriver.common.by import By
from sites.amz.decaptcha import Decaptcha
from sites.exception import TimeoutException, CaptchaException, StepFailed
from .amz_base import AmzBase


class Register(AmzBase):
    _search_bar = (By.XPATH, './/*[@id=\'twotabsearchtextbox\']')
    _signin_new_acct = (By.ID, 'createAccountSubmit')
    _reg_form = (By.ID, 'ap_register_form')
    _reg_user = (By.ID, 'ap_customer_name')
    _reg_email = (By.ID, 'ap_email')
    _reg_email_check = (By.ID, 'ap_email_check')
    _reg_password = (By.ID, 'ap_password')
    _reg_password_check = (By.ID, 'ap_password_check')
    _reg_submit = (By.ID, 'continue')
    _reg_captcha = (By.ID, 'auth-captcha-image')
    _reg_captcha_guess = (By.ID, 'auth-captcha-guess')
    _reg_telephone = (By.ID, 'ap_customer_name_pronunciation')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        # self.url = self.url_tmpl.format(**{'market': self.url})

    def navigate(self):
        def _check():
            return self.find_element(*self._signin_new_acct)

        create_new_acct = self.find_element(*self._signin_new_acct)
        if not create_new_acct:
            raise StepFailed('Cannot find the ''create an account button''')

        self.click(self._signin_new_acct)
        return True

    def is_done(self):
        return self.find_element(*self._search_bar) is not None

    def process(self):
        def _check():
            return self.find_element(*self._reg_form)

        def _do():
            user = self.wait_valid_element(self._reg_user)
            email = self.wait_valid_element(self._reg_email)
            email_chk = self.find_element(*self._reg_email_check)
            telephone = self.find_element(*self._reg_telephone)

            password = self.wait_valid_element(self._reg_password)
            password_chk = self.wait_valid_element(self._reg_password_check)

            user.clear()
            user.send_keys('%s %s' % (self.account.get('given_name'),
                                      self.account.get('surname')))

            if telephone:
                telephone = self.wait_valid_element(self._reg_telephone)
                telephone.clear()
                telephone.send_keys(self.account.get('telephone'))

            email.clear()
            email.send_keys(self.account.get('email'))
            if email_chk:
                email_chk = self.wait_valid_element(self._reg_email_check)
                email_chk.clear()
                email_chk.send_keys(self.account.get('email'))
            password.clear()
            password.send_keys(self.account.get('password'))
            password_chk.clear()
            password_chk.send_keys(self.account.get('password'))

            self.click(self._reg_submit)

        def _timeout():
            raise TimeoutException('Failed to visit register form')

        self.check_and_do(60, _check, _do, _timeout)


class RegisterWithCaptcha(AmzBase):

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.reg = Register(driver, params, account)
        self.decaptcha = Decaptcha(driver, params, account,
                                   lambda: self.reg.process)

    def is_done(self, timeout=30):
        def _check():
            return self.reg.is_done()
        return self.check_and_do(timeout, _check, _check, _check)

    def navigate(self):
        self.reg.navigate()
        return True

    def process(self):
        self.reg.process()

        if self.reg.is_done():
            return

        retry_cnt = 0
        while self.decaptcha.has_met_captcha():
            if retry_cnt > 10:
                raise CaptchaException('Failed to decaptcha')

            self.decaptcha.process()
            self.reg.process()
