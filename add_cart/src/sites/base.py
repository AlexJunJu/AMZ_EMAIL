# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import os
import time
import json
import logging as log
from StringIO import StringIO
from PIL import Image
from deathbycaptcha import SocketClient
from sites.exception import LoadPageFailed, StepFailed, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (NoSuchElementException,
                                        InvalidElementStateException)
reload(sys)
sys.setdefaultencoding('utf8')


class MyDecapcha:

    def __init__(self):
        self.user = 'nelliecsparkstgj'
        self.passwd = 'AAbb1122'
        self.client = SocketClient(self.user, self.passwd)
        self.client.is_verbose = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.client.close()
        except Exception:
            log.exception('Failed to close dbc client')

    def decode(self, fn, timeout=60):
        try:
            captcha = self.client.decode(fn, timeout=timeout)
            return captcha['text'].strip()
        except Exception:
            log.exception('Failed to decode')
            return None


class BaseStep(object):
    url = None

    _need_refresh_msgs = ['The requested URL could not be retrieved',
                          'Problem loading page']

    def __init__(self, driver, params):
        self.driver = driver
        self.params = params
        self._deathbycaptcha_client = None

    def is_firefox(self):
        return self.driver.name == 'firefox'

    def is_chrome(self):
        return self.driver.name == 'chrome'

    def navigate(self):
        """
        Visit a specific URL
        """
        self.driver.get(self.url)

        return True

    def process(self):
        """
        Process a specific functionality, e.g. sign in/sign out
        """
        pass

    def is_done(self, timeout=0):
        """
        check the process is done or not
        """
        return True

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None

    def find_elements(self, by, value):
        try:
            return self.driver.find_elements(by, value)
        except NoSuchElementException:
            return None

    def find_alternative_elem(self, elem_list):
        for elem in elem_list:
            elem_to_find = self.find_element(*elem)
            if elem_to_find:
                return elem_to_find
        return None

    def find_visible_elem(self, elem_list):
        for elem in elem_list:
            if self.is_visible(elem):
                return self.find_element(*elem)
        return None

    def wait_valid_element(self, by_loc, wait_time=3):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        return WebDriverWait(self.driver, wait_time).\
            until(EC.element_to_be_clickable(by_loc))

    def wait_visible_element(self, by_loc, wait_time=3):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        return WebDriverWait(self.driver, wait_time).\
            until(EC.visibility_of_element_located(by_loc))

    def is_visible(self, by_loc, wait_time=1):
        try:
            return self.wait_visible_element(by_loc, wait_time) is not None
        except Exception:
            return False

    def is_valid(self, by_loc, wait_time=1):
        try:
            return self.wait_valid_element(by_loc, wait_time) is not None
        except Exception:
            return False

    def is_valid_elem(self, element, wait_time=1):
        from selenium.webdriver.support.ui import WebDriverWait

        def gen_element_to_be_clickable(element):
            def _do(driver):
                if element and element.is_displayed() and element.is_enabled():
                    return element
                else:
                    return False  # it is the rule in EC

            return _do
        try:
            return WebDriverWait(self.driver, wait_time).\
                until(gen_element_to_be_clickable(element)) is not None
        except Exception:
            return False

    def click(self, by_loc, wait_time=3):
        element = self.wait_valid_element(by_loc, wait_time)
        element.click()

    def click_elem(self, element, wait_time=3):
        from selenium.webdriver.support.ui import WebDriverWait

        def gen_element_to_be_clickable(element):
            def _do(driver):
                if element and element.is_displayed() and element.is_enabled():
                    return element
                else:
                    return False  # it is the rule in EC

            return _do

        element = WebDriverWait(self.driver, wait_time).\
            until(gen_element_to_be_clickable(element))
        element.click()

    def need_refresh_page(self):
        for msg in self._need_refresh_msgs:
            if msg in self.driver.title:
                return True
        return False

    def check_and_do(self, expire, check, process, process_timeout=None):
        expired_time = int(time.time()) + expire
        while True:
            if self.need_refresh_page():
                log.info('Meet msg %s,try to refresh' % self.driver.title)
                self.driver.refresh()

            try:
                if check():
                    return process()
            except NoSuchElementException:
                pass

            if time.time() >= expired_time:
                break

            time.sleep(2)

        if self.need_refresh_page():
            raise LoadPageFailed('Meet title %s' % self.driver.title)

        if process_timeout:
            process_timeout()

    def select_by_value(self, by_loc, value, wait_time=5, step_time_gap=0.2,
                        retry_cnt=3):
        def _do():
            elem = self.wait_valid_element(by_loc, wait_time)
            elem.location_once_scrolled_into_view
            select_elem = Select(elem)
            time.sleep(step_time_gap)
            select_elem.select_by_value(value)

        for i in xrange(0, retry_cnt):
            try:
                _do()
                return True
            except InvalidElementStateException:
                continue
        else:
            return False

    def select_elem_by_value(self, elem, value, wait_time=5, step_time_gap=0.2,
                             retry_cnt=3):
        def _do():
            elem.location_once_scrolled_into_view
            select_elem = Select(elem)
            time.sleep(step_time_gap)
            select_elem.select_by_value(value)

        for i in xrange(0, retry_cnt):
            try:
                _do()
                return True
            except InvalidElementStateException:
                continue
        else:
            return False

    def rect(self, elem):
        js = '''
function Coords(el) {
    this.left = parseInt(el.offset().left);
    this.top = parseInt(el.offset().top);
    this.right = parseInt(this.left + el.outerWidth());
    this.bottom = parseInt(this.top + el.outerHeight());
}

Coords.prototype.toString = function () {
    var x = Math.max(this.left, 0);
    var y = Math.max(this.top, 0);
    return JSON.stringify({
        x:x - $(window).scrollLeft(),
        y:y - $(window).scrollTop(),
        width:this.right - x,
        height:this.bottom - y
    });
};

return (new Coords($(arguments[0]))).toString();
        '''
        return json.loads(self.driver.execute_script(js, elem))

    def analyse_captcha(self, captcha_img):
        rect = self.rect(captcha_img)
        img = self.driver.get_screenshot_as_png()
        with Image.open(StringIO(img)) as img_screen:
            img_captcha = img_screen.crop((rect['x'],
                                           rect['y'],
                                           rect['x'] + rect['width'],
                                           rect['y'] + rect['height']))

            time_stamp = time.time()

            # XXX: shall use BytesIO instead a actual file
            img_file = './captcha_%s.png' % (time_stamp)
            img_captcha.save(img_file)
            try:
                with MyDecapcha() as decaptcha:
                    return decaptcha.decode(img_file)
            finally:
                os.remove(img_file)

    def move_to_elem_js(self, elem):
        js = '''
            var elem = arguments[0];
            elem.scrollIntoView(true);
        '''
        self.driver.execute_script(js, elem)

    def send_keys_to_elem_js(self, elem, keys):
        js = '''
            var elems = document.getElementsByName(arguments[0]);
            elems[0].value = arguments[1];
        '''
        self.driver.execute_script(js, elem, keys)

    def send_keys_to_elem(self, element, keys, wait_time=3):
        from selenium.webdriver.support.ui import WebDriverWait

        def gen_element_to_be_clickable(element):
            def _do(driver):
                if element and element.is_displayed() and element.is_enabled():
                    return element
                else:
                    return False  # it is the rule in EC

            return _do

        element = WebDriverWait(self.driver, wait_time).\
            until(gen_element_to_be_clickable(element))
        element.clear()
        element.send_keys(keys)

    def send_keys(self, by_loc, keys, wait_time=3):
        element = self.wait_valid_element(by_loc, wait_time)
        element.clear()
        element.send_keys(keys)

    def page_home(self):
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.HOME)
        actions.perform()

    def page_down(self):
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()

    def make_step_failed(self, msg):
        return StepFailed('%s, %s' % (self.__class__.__name__, msg))

    def make_timeout(self, msg):
        return TimeoutException('%s, %s' % (self.__class__.__name__, msg))
