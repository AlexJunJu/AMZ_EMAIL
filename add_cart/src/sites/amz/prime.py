from __future__ import absolute_import

import logging as log
import time
import random
from selenium.webdriver.common.by import By
from .amz_base import AmzBase


class PrimeStep(AmzBase):
    _nav_link_your_account = [(By.ID, 'nav-link-yourAccount'),
                              (By.ID, 'nav-link-accountList')]
    _end_prime_link = \
        (By.XPATH,
         '//*[@id="primeCentralResponsiveHomePageLinksContentFromMS3"]' +
         '/div/div[2]/a')

    def __init__(self, driver, params, account):
        AmzBase.__init__(self, driver, params)
        self.account = account
        self.is_prime = "UNKNOWN"

    def validate(self):
        return True

    def navigate(self):
        # goto account dashboard
        account_link = self.find_alternative_elem(self._nav_link_your_account)
        self.click_elem(account_link, wait_time=5)

        # goto payment
        self.click((By.XPATH, '//div[@data-card-identifier="Prime"]'),
                   wait_time=5)
        time.sleep(3 + random.randint(1, 4))

        return True

    def process(self):
        self.is_prime = '%s' % self.is_visible(self._end_prime_link)


class DisablePrime(PrimeStep):
    def __init__(self, driver, params, account):
        PrimeStep.__init__(self, driver, params, account)

    def process(self):
        if not self.is_visible(self._end_prime_link):
            raise self.make_step_failed(
                '%s is not prime yet' % self.account.get('email'))

        self.click(self._end_prime_link)

        # the first continue
        _continue = (By.ID, 'continue-btn')
        if self.is_visible(_continue):
            self.click(_continue, wait_time=2)

        # the second continue
        if self.is_visible(_continue):
            self.click(_continue, wait_time=2)

        # final end_membership
        _end_membership = (By.ID, 'endMembershipNowBtn')
        self.click(_end_membership, wait_time=3 + random.randint(1, 4))

        # double check the membership
        if self.is_visible(self._end_prime_link):
            raise self.make_step_failed(
                '%s is still prime yet' % self.account.get('email'))

        log.warn('Succeed to revoke prime from %s.' % self.account.get('email'))


class EnablePrime(PrimeStep):
    def __init__(self, driver, params, account):
        PrimeStep.__init__(self, driver, params, account)

    def process(self):
        # Check whether the current account is prime or not
        if self.is_visible(self._end_prime_link):
            log.info('%s is already a prime member in %s' % (
                self.account.get('email'),
                self.params.get('marketplace_url')))
            return

        # go to prime sign up page
        _prime_promotion_link = (
            By.XPATH,
            '//*[@id="primeCentralHomepagePromotionSlot' +
            'ContentImportedFromMS3"]/div/div/div/div/div/a')
        self.click(_prime_promotion_link)
        time.sleep(3 + random.randint(1, 4))

        # start 30 days Prime free trial
        _not_a_student = (By.XPATH, '//*[@id="toggle-bar"]/div/a')
        if self.is_visible(_not_a_student):
            self.click(_not_a_student)

        _button_prime = (By.XPATH,
                         '//*[@id="primeDetailPage"]/div[1]/div/div/form/span')
        self.click(_button_prime)
        time.sleep(3 + random.randint(1, 4))

        # confirm prime
        _add_new_card = (By.XPATH,
                         '//div[@data-a-expander-name="pmts-add-new-card"]')
        if self.is_visible(_add_new_card):
            raise self.make_step_failed('Missing credit card.')

        _prime_signup = \
            (By.XPATH,
             '//*[@id="a-page"]/div[4]/div[3]/div[3]/div/div/div[1]/span')
        if not self.is_visible(_prime_signup, wait_time=2):
            raise self.make_step_failed('Signup button is not visibled')

        self.click(_prime_signup)

        # check the prime status
        time.sleep(5 + random.randint(1, 4))
        self.navigate()
        time.sleep(3 + random.randint(1, 4))
        if not self.is_visible(self._end_prime_link):
            raise self.make_step_failed('Failed to activate Prime trial.')

        log.warn('Succeed to activate 30 days Prime trial for %s.' %
                 self.account.get('email'))
