# -*- coding: utf-8 -*-
import sys
import os
import io
import subprocess
import time
import logging
import random
import json
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from sites.amz import (amz_account_register, amz_bind_credit_card,
                       amz_add_to_cart, amz_clear_cart, amz_add_address,
                       amz_create_order, amz_enable_prime, amz_disable_prime,
                       amz_bind_credit_card_prime, amz_check_account)
from model import (AmzAccountInfo, AmzSaleFarmRealAddress, AmzDebitCard)

reload(sys)
sys.setdefaultencoding('utf8')

# log.basicConfig(filename='./logs/farm.log', level=log.INFO)
logfile = './logs/farm.log'
log = logging.getLogger('')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = RotatingFileHandler(logfile, maxBytes=(1048576*5), backupCount=5)
fh.setFormatter(format)
log.addHandler(fh)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    log.error("Uncaught exception",
              exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_uncaught_exception


class MyDriver:

    def __init__(self, profile_id, host='127.0.0.1', port=35000):
        self.profile_id = profile_id
        self.url = 'http://' + host + ':' + str(port) + '/api/v1/webdriver'
        capabilities = {'multiloginapp-profileId': self.profile_id}
        self.driver = webdriver.Remote(command_executor=self.url,
                                       desired_capabilities=capabilities)

    def __enter__(self):
        log.info('driver %s enter' % self.profile_id)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.driver:
            log.info('driver %s exit with NULL driver' % self.profile_id)
            return

        try:
            self.driver.close()
            self.driver.quit()
        except Exception:
            log.exception('Failed to quit driver')
        finally:
            log.info('driver %s exit' % self.profile_id)


def _gen_randomword(string_data):
    def _do(length):
        result = ''.join(random.choice(string_data) for i in range(length))
        return result[1:] + result[0] if result[0] \
            in ['_', '@', '!', '#', '~'] else result
    return _do


_name_data = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
_random_name = _gen_randomword(_name_data)

_passwd_data = '1234567890abcdefghijklmnopqrstuvwxyz' + \
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ_@!#~'
_random_passwd = _gen_randomword(_passwd_data)


class FarmTask(object):

    FARM_REG = 1
    FARM_BIND_CREDIT_CARD = 2
    FARM_ENABLE_PRIME = 3
    FARM_DISABLE_PRIME = 4
    FARM_ADD_TO_CART = 5
    FARM_CLEAR_CART = 6
    FARM_ADD_ADDRESS = 7
    FARM_ORDER = 8
    FARM_BIND_CREDIT_CARD_PRIME = 9
    FARM_CHECK_ACCOUNT = 10

    ASIN_MAP = {}
    TIME_GAP = 3600

    def __init__(self, task_type, params, max_tries=3):
        self.task_type = task_type
        self.params = params
        self.account = get_account(self.params.get('account_id'))
        self._max_tries = max_tries
        self._run_times = 0

    def can_run(self):
        if self.task_type != self.FARM_ORDER:
            return True

        current_time = time.time()
        asin_str = self.params['asin']
        asin_list = asin_str.split('\t')
        for asin in asin_list:
            if not asin or not asin.strip():
                continue

            last_time = self.ASIN_MAP.get(asin, 0)
            time_gap = random.uniform(self.TIME_GAP, self.TIME_GAP * 1.2)
            if current_time - last_time <= time_gap:
                return False
        else:
            for asin in asin_list:
                self.ASIN_MAP[asin] = current_time

        return True

    def reset_timer(self):
        if self.task_type != self.FARM_ORDER:
            return

        asin_str = self.params['asin']
        asin_list = asin_str.split('\t')
        for asin in asin_list:
            if not asin or not asin.strip():
                continue
            self.ASIN_MAP[asin] = 0

    def is_idempotent(self):
        return self.task_type in [self.FARM_ENABLE_PRIME,
                                  self.FARM_DISABLE_PRIME,
                                  self.FARM_ADD_TO_CART,
                                  self.FARM_CLEAR_CART,
                                  self.FARM_ADD_ADDRESS,
                                  self.FARM_ORDER]

    def get_mla_profile(self):
        return self.account.get('mla_profile')

    def register(self, driver):
        amz_account_register(driver, self.account, self.params)

    def bind_credit_card(self, driver):
        amz_bind_credit_card(driver, self.account, self.params)

    def enable_prime(self, driver):
        amz_enable_prime(driver, self.account, self.params)

    def disable_prime(self, driver):
        amz_disable_prime(driver, self.account, self.params)

    def bind_credit_card_prime(self, driver):
        amz_bind_credit_card_prime(driver, self.account, self.params)

    def add_to_cart(self, driver):
        amz_add_to_cart(driver, self.account, self.params)

    def clear_cart(self, driver):
        amz_clear_cart(driver, self.account, self.params)

    def add_address(self, driver):
        amz_add_address(driver, self.account, self.params)

    def order(self, driver):
        amz_create_order(driver, self.account, self.params)

    def check_account(self, driver):
        amz_check_account(driver, self.account, self.params)

    def process(self, driver):
        self._run_times += 1
        if self._max_tries == self._run_times:
            log.error('Too many retirs, not to try any more')
            return

        if not self.account:
            log.error('Failed to get the account by %s' % self.params)
            return

        processor_map = {
            self.FARM_REG: self.register,
            self.FARM_BIND_CREDIT_CARD: self.bind_credit_card,
            self.FARM_ENABLE_PRIME: self.enable_prime,
            self.FARM_DISABLE_PRIME: self.disable_prime,
            self.FARM_BIND_CREDIT_CARD_PRIME: self.bind_credit_card_prime,
            self.FARM_ADD_TO_CART: self.add_to_cart,
            self.FARM_CLEAR_CART: self.clear_cart,
            self.FARM_ADD_ADDRESS: self.add_address,
            self.FARM_ORDER: self.order,
            self.FARM_CHECK_ACCOUNT: self.check_account,
            }

        processor = processor_map.get(self.task_type, None)
        if not processor:
            log.error('Invalid task type %s' % self.task_type)
            return False

        addr = get_addr(self.params.get('addr_id'))
        if addr:
            self.params['addr_info'] = addr

        credit_card = get_credit_card(self.params.get('credit_card_id'))
        if credit_card:
            self.params['credit_card_info'] = credit_card
            credit_card_addr = get_addr(credit_card.get('addr_id'))
            if credit_card_addr:
                self.params['credit_card_addr_info'] = credit_card_addr

        try:
            log.info('Start processing %s account %s, round %s' % (
                processor.__name__, self.account.get('email'), self._run_times))
            return processor(driver)
        finally:
            log.info('Finish processing %s account %s' % (
                processor.__name__, self.account.get('email')))


class MultiloginAppMgr:

    def __init__(self):
        self.exec_file = 'C:\Program Files (x86)\Multiloginapp' + \
                         '\multiloginapp.exe'
        self.process = None

    def __enter__(self):
        log.info('Start MultiloginApp')
        self.process = subprocess.Popen([self.exec_file])
        time.sleep(random.randint(20, 40))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        log.info('Stop MultiloginApp')
        self.process.terminate()
        time.sleep(random.randint(20, 40))
        img_name = 'browser-chrome-driver-2.27-win64.bin'
        cmd = 'taskkill /f /im "%s" /FI "IMAGENAME eq %s"' % (img_name,
                                                              img_name)
        log.info(cmd)
        os.system(cmd)

    @classmethod
    def process(cls, task_list, time_gap=None, max_count_down=5):
        while len(task_list) > 0:
            count_down = max_count_down
            with MultiloginAppMgr():
                while len(task_list) > 0:
                    task = task_list.pop()
                    if not task.can_run():
                        task_list.insert(0, task)
                        time.sleep(random.uniform(1, 10))
                        continue

                    try:
                        with MyDriver(task.get_mla_profile()) as driver:
                            task.process(driver.driver)
                    except Exception as ex:
                        log.exception('Failed run %s with %s due to %s' % (
                            task.task_type, task.params, ex))
                        if task.is_idempotent():
                            task.reset_timer()
                            task_list.insert(0, task)
                        time.sleep(random.uniform(10, 60))
                    finally:
                        count_down -= 1
                        if count_down == 0:
                            break


def _gen_get_account():
    lines = None
    with io.open('./conf/account.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()

    json_data = json.loads(lines)
    account_list = []

    profile_rel = {}
    addr_rel = {}
    prj_rel = {}
    gift_card_rel = {}
    credit_card_rel = {}

    for data in json_data:
        account_list.append(
            AmzAccountInfo(
                id=data.get('id'),
                market_place_id=data.get('market_place_id'),
                email=data.get('email'),
                password=data.get('password'),
                given_name=data.get('given_name'),
                surname=data.get('surname'),
                telephone=data.get('telephone'),
                telephones=data.get('telephones', ''),
            ))
        profile_rel[data.get('email')] = data.get('mla_profile')
        addr_rel[data.get('email')] = data.get('addr_id')
        prj_rel[data.get('email')] = {'asin': data.get('asin'),
                                      'keywords': data.get('keywords'),
                                      'promotion': data.get('promotion'),
                                      'brand': data.get('brand'),
                                      'price': data.get('price', 0)}
        gift_card_rel[data.get('email')] = data.get('gift_card')
        credit_card_rel[data.get('email')] = data.get('credit_card_list')

    account_map = {account.id: account for account in account_list}

    # XXX @TODO, profile list is hard coded.
    # mla_profile_list = load_profiles()
    # profile_list = [profile.profile_id for profile in mla_profile_list
    #                 if profile.country == 'de' and profile.id >= 120]  # <==

    def _get_account(account_id):
        account = account_map.get(account_id, None)
        if not account:
            return None

        data = account.to_json()
        data['mla_profile'] = profile_rel[account.email]
        data['addr_id'] = addr_rel[account.email]
        data['prj'] = prj_rel[account.email]
        data['gift_card'] = gift_card_rel[account.email]
        data['credit_card_list'] = credit_card_rel[account.email]
        return data

    def _get_account_list():
        return account_list

    return _get_account, _get_account_list


get_account, get_account_list = _gen_get_account()


def _gen_get_credit_card():
    lines = None
    with io.open('./conf/credit_card.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()

    card_used_by_map = {}
    json_data = json.loads(lines)
    card_list = []
    for data in json_data:
        amz_debit_card = AmzDebitCard(
                id=data.get('id'),
                source=data.get('source'),
                email=data.get('email'),
                password=data.get('password'),
                card_holder=data.get('card_holder'),
                card_number=data.get('card_number'),
                telephone=data.get('telephone'),
                expired_date=data.get('expired_date'),
                addr_id=data.get('addr_id'),
                balance=data.get('balance'),
                currency=data.get('currency'),
                used_by=data.get('used_by'),
            )
        card_list.append(amz_debit_card)
        card_used_by_map[data['used_by_email']] = amz_debit_card

    card_map = {card.id: card for card in card_list}

    def _get_card(card_id):
        card = card_map.get(card_id, None)
        return card.to_json() if card else None

    def _get_card_by_account(email):
        card = card_used_by_map.get(email, None)
        return card.to_json() if card else None

    return _get_card, _get_card_by_account


get_credit_card, get_credit_card_by_acct = _gen_get_credit_card()


def _gen_get_addr():
    lines = None
    with io.open('./conf/address.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()

    json_data = json.loads(lines)
    address_list = []
    for data in json_data:
        address_list.append(
            AmzSaleFarmRealAddress(
                id=data.get('id'),
                given_name=data.get('given_name'),
                surname=data.get('surname'),
                telephone=data.get('telephone'),
                country=data.get('country'),
                state=data.get('state'),
                city=data.get('city'),
                address_line1=data.get('address_line1'),
                address_line2=data.get('address_line2'),
                zip_code=data.get('zip_code'),
                gate_code=data.get('gate_code'),
            ))

    addr_map = {addr.id: addr for addr in address_list}

    def _get_addr(addr_id):
        addr = addr_map.get(addr_id, None)
        if not addr:
            return None

        return addr.to_json()

    return _get_addr


get_addr = _gen_get_addr()


if __name__ == "__main__":
    # from ipdb import set_trace
    # set_trace()

    misc_map = {
        'B01MXYEEZS': {
            'gift_card': {'top_up_amount': 12.9},
        },
        'B0746C2RVX': {
            'gift_card': {'top_up_amount': 9},
            'variants': ['B0746C2RVX', 'B0718TYY5P'],
        },
        # 'B0747L38Q9': {
        #     'gift_card': {'top_up_amount': 9},
        #     'variants': ['B0747L38Q9', 'B0747KQ6ZP'],
        # },
        # 'B0747KQ6ZP': {
        #     'gift_card': {'top_up_amount': 9},
        #     'variants': ['B0747L38Q9', 'B0747KQ6ZP'],
        # },
        'B01LXMBZ0N': {
            'gift_card': {'top_up_amount': 9},
            'variants': ['B01LXMBZ0N', 'B074CQY1DT', 'B0722KDD1C',
                         'B0722K8PMQ'],
        },
    }

    exit_nodes = ['B072NYB9GH', 'B0734TCG2L', 'B00RTL31BI', 'B00RTL31BI',
                  'B01LYN8CNK', 'B06XRWV3VB']

    def _make_task(task_type, account_id):
        acct = get_account(account_id)
        card = get_credit_card_by_acct(acct['email'])
        prj = acct['prj']
        # gift_card = misc_map[prj['asin']]['gift_card']
        return FarmTask(task_type,
                        params={
                            'market_place_id': 4,
                            'account_id': account_id,
                            'credit_card_id':
                                card.get('id', '') if card else '',
                            'addr_id': acct.get('addr_id', ''),
                            'is_adult': True,
                            'brand': prj.get('brand'),
                            'asin': prj.get('asin', ''),
                            'keywords': prj.get('keywords', ''),
                            'variants': misc_map,
                            'actual_price': prj.get('price', ''),
                            'promotion': prj.get('promotion', ''),
                            'gift_card': {
                                'gift_card': acct.get('gift_card', '')},
                            'entry_node': random.choice(exit_nodes),
                            'exit_node': random.choice(exit_nodes)
                        })

    def _gen_time_gap(task_type):
        def _time_gap_default():
            return random.randint(0, 1 * 10)

        def _time_order_gap():
            return random.randint(60 * 60, 120 * 60)

        return _time_order_gap if task_type == FarmTask.FARM_ORDER\
            else _time_gap_default

    acct_list = get_account_list()

    email_skip_list = [
    ]
    if email_skip_list:
        acct_list = [acct for acct in acct_list
                     if acct.email not in email_skip_list]

    email_redo_list = [
        # 'Yx_cWgpayhsP@yahoo.com', # unknown error
        # 'xKLz9EtgITh@icloud.com',  # Failed to input gift card
        # 'vxuoS1oUHGx@yandex.com', # phone number error
        # 'Pmiz5JBk@us.ibm.com',
        # 'QIoGa6wpvTpM@sina.com', # Done
        # 'QKzZPjuX9@mac.com',
        # 'qPh2PfndloPg@icloud.com',
        # 'RfJlEiSZ4FS@yandex.com',
        # 'sMXA_oeFz_QE@inbox.com',
        # 'UOyWGj11PvUz@us.ibm.com', # unknown error Wrong password
        # 'UQZnhBr2rOIB@me.com',
        # 'v9o3yLMV@sina.com',
        'WxPI23Umo@yandex.com',
    ]
    if email_redo_list:
        acct_list = [acct for acct in acct_list
                     if acct.email in email_redo_list]

    # task_list = [
    #     _make_task(FarmTask.FARM_BIND_CREDIT_CARD_PRIME, account.id)
    #     for account in acct_list
    # ]

    # task_list = [
    #     _make_task(FarmTask.FARM_DISABLE_PRIME, account.id)
    #     for account in acct_list
    # ]

    # task_list = [
    #     _make_task(FarmTask.FARM_CHECK_ACCOUNT, account.id)
    #     for account in acct_list
    # ]

    task_list = [
        _make_task(FarmTask.FARM_ORDER, account.id) for account in acct_list]

    if task_list[0].task_type == FarmTask.FARM_ORDER:
        random.shuffle(task_list)
    else:
        task_list.reverse()
    set_trace()
    MultiloginAppMgr.process(task_list,
                             time_gap=_gen_time_gap(task_list[0].task_type))
    print 'DONE'
