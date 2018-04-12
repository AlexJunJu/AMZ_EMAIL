# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import requests
import random
import json
reload(sys)
sys.setdefaultencoding('utf8')


class UserAgent(object):
    def __init__(self, file_name):
        self.ua_list = None
        with open(file_name, 'r') as fp:
            self.ua_list = [l.strip() for l in fp.readlines()]

        self.ua_list_bak = []

    def choose(self):
        if not self.ua_list:
            self.ua_list = self.ua_list_bak
            self.ua_list_bak = []

        random.shuffle(self.ua_list)
        ua = self.ua_list.pop()
        self.ua_list_bak.append(ua)
        return ua


_UA = UserAgent('./tools/user_agent.txt')


def weighted_choice(choices):
    total = sum(w for c, w in choices.iteritems())
    rand = random.uniform(0, total)
    upto = 0
    for c, w in choices.iteritems():
        if upto + w >= rand:
            return c
        upto += w


class Screen(object):
    POPULAT_SCREENS = {
        (1366, 768): 20,
        (1920, 1080): 6,
        (1280, 800): 10,
        (1440, 900): 8,
        (1280, 1024): 8,
        (1600, 900): 8,
        (1024, 768): 10,
        (1680, 1050): 8,
        (1920, 1200): 6,
        (1360, 768): 6,
        (1280, 720): 6,
        }

    @classmethod
    def choose(cls):
        return weighted_choice(cls.POPULAT_SCREENS)


class Timezone(object):

    # @TODO need to complete the timezone in country
    TIMEZONE = {
        'de': {'Europe/Berlin': 2, 'Europe/Busingen': 1},
        'uk': {'Europe/London': 1},
        'fr': {'Europe/Paris': 1},
        'it': {'Europe/Rome': 1},
        'es': {'Europe/Madrid': 1},
        'us': {'America/New_York': 20,
               'America/Los_Angeles': 20,
               'America/Chicago': 20,
               'America/Phoenix': 20,
               'America/Indiana/Indianapolis': 10,
               'America/Detroit': 15,
               'America/Denver': 15},
        'ca': {'America/Toronto': 20,
               'America/Vancouver': 15,
               'America/Edmonton': 10},
        'jp': {'Asia/Tokyo': 1},
        }

    @classmethod
    def choose(cls, country):
        if country not in cls.TIMEZONE:
            country = random.choice(cls.TIMEZONE.keys())
        return weighted_choice(cls.TIMEZONE.get(country))


def create_profile(token, name, country, proxy_host, proxy_port, ua=None,
                   browser_type='chrome', time_zone=None):
    url = 'https://api.multiloginapp.com/v1/profile/create?token=%s' % token
    weight, height = Screen.choose()

    params = {
        'name': name,
        'browserType': browser_type,  # firefox, chrome, opera, stealth_fox
        'proxyHost': proxy_host,
        'proxyPort': proxy_port,
        # 'proxyUser': 'username',
        # 'proxyPass': '***',
        # 'proxyIpValidation': true,
        'proxyType': 'http',  # http, socks4, socks5
        'notes': 'notes text',
        'userAgent': ua if ua else _UA.choose(),
        'disablePlugins': True,
        'disableWebrtcPlugin': True,
        'disableFlashPlugin': True,
        # 'customExtensionFileNames': 'ext1.crx;ext2.crx',
        'useZeroFingerprints': True,
        'generateZeroFingerprintsData': True,
        'canvasDefType': 'noise',  # noise, block
        # 'platform': 'Win32',
        'doNotTrack': '0',
        # 'hardwareConcurrency': 8,
        'langHdr': 'en-US',
        'screenHeight': height,
        'screenWidth': weight,
        'timeZone': time_zone if time_zone else Timezone.choose(country),
        'tag': country
        }

    # from pprint import pprint
    # pprint(params)
    # json_str = json.dumps(params, separators=(',', ':'))
    session = requests.session()
    # set_trace()
    request = session.post(url,
                           json=params,  # data={'json': json_str},
                           verify=False,
                           headers={
                               'User-Agent': ua,
                               'Content-Type': 'application/json',
                               'Accept': 'application/json',
                           })
    return json.loads(request.content)


if __name__ == '__main__':
    from ipdb import set_trace
    set_trace()

    import time

    token = '9db675c858ac1e68e3237d191283ca2f5fb63c04'
    # print create_profile(token, 'ake_test_1', 'de', '127.0.0.1', '1234',
    #                      browser_type='chrome')
    # print create_profile(token, 'ake_test_2', 'de', '127.0.0.1', '1235',
    #                      browser_type='stealth_fox')

    from model import MlaProfile

    profile_list = []
    browser = MlaProfile._BROWSER_CHROME
    market_id = 7
    country = 'ca'
    for i in xrange(1001, 1021):
        profile_list.append(MlaProfile(
            id=i, market_place_id=market_id, country=country,
            name='%s_%s_%05d' % (country, browser, i), browser=browser,
            proxy_host='127.0.0.1', proxy_port=24000 + i))

    data_list = []
    for profile in profile_list:
        time.sleep(5)
        result = create_profile(token, name=profile.name,
                                country=profile.country,
                                proxy_host=profile.proxy_host,
                                proxy_port=profile.proxy_port)
        if result.get('status') == 'OK':
            profile.profile_id = result.get('value')
        else:
            continue

        data = {k: v for k, v in profile.__dict__.iteritems()
                if k != '_sa_instance_state'}
        data_list.append(data)

    lines = json.dumps(data_list, indent=2)
    with open('./logs/out/profiles.conf', 'w+') as fp:
        fp.write(lines)
