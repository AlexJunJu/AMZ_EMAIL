from __future__ import absolute_import

import time
import os
from selenium.webdriver.common.by import By
from StringIO import StringIO
from PIL import Image
from sites.exception import CaptchaException
from .amz_base import AmzBase


class Decaptcha(AmzBase):
    _sigin_captcha = (By.ID, 'auth-captcha-image')
    _sigin_captcha_guess = (By.ID, 'auth-captcha-guess')

    def __init__(self, driver, params, account, on_success):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.on_success = on_success

    def navigate(self):
        return True

    def get_captcha(self):
        return self.find_element(*self._sigin_captcha)

    def has_met_captcha(self):
        return self.get_captcha() is not None

    def process(self):
        def _on_success(guessed_captcha):
            guess = self.wait_valid_element(self._sigin_captcha_guess)
            guess.clear()
            guess.send_keys(guessed_captcha)
            self.on_success()

        captcha = self.get_captcha()
        if not captcha:
            return

        if self.is_chrome():
            raise CaptchaException('Please try using Firefox to decaptcha')

        for i in xrange(0, 3):
            resolution = self.analyse_captcha(self, captcha)
            _on_success(resolution)

            captcha = self.get_captcha()
            if not captcha:
                return
        raise CaptchaException('Please failed to decaptcha')
