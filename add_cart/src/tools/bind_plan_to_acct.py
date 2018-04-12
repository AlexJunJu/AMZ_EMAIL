# -*- coding: utf-8 -*-
import sys
import io
import json
# import logging as log
# from iso_country_codes import get_country
from collections import OrderedDict
from model import MlaProfile
from utils import gen_start_id

reload(sys)
sys.setdefaultencoding('utf8')


def load_profiles():
    lines = None
    with open('./conf/profiles.conf') as fp:
        lines = fp.read()

    json_data = json.loads(lines)
    profile_list = []
    for data in json_data:
        profile_list.append(
            MlaProfile(id=data.get('id'),
                       market_place_id=data.get('market_place_id'),
                       country=data.get('country'),
                       name=data.get('name'),
                       profile_id=data.get('profile_id'),
                       browser=data.get('browser'),
                       proxy_host=data.get('proxy_host'),
                       proxy_port=data.get('proxy_port'),
                       ))

    return profile_list


def get_data_list_from_tsv(file_name, start_id=None):
    lines = None
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    data_list = []
    headers = [col.strip() for col in lines[0].split('\t') if col.strip()]

    for i in xrange(1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        data = OrderedDict()
        tokens = line.split('\t')
        for j in xrange(len(headers)):
            data[headers[j]] = tokens[j] if j < len(tokens) else ''

        if start_id:
            data['id'] = start_id + i - 1

        data_list.append(data)

    return data_list


def get_card_list(data_list):
    card_list = []
    for i in xrange(len(plan_list)):
        card = OrderedDict()
        data = plan_list[i]
        if not data.get('card_number'):
            continue

        card['id'] = start_id + i
        email = data['used_by']
        card['email'] = data['binded_email']
        card['password'] = data['binded_passwd']
        card['card_holder'] = '%s %s' % (data['given_name'], data['surname'])
        card['card_number'] = data['card_number']
        card['telephone'] = data['telephone']
        order_num = data['order_num']
        card['addr_id'] = order_addr_map[order_num]['id']
        card['card_number'] = data['card_number']
        card['valid_period'] = data['valid_period']
        card['CVV'] = data['CVV']
        card['expired_date'] = data['expired_date']
        card['balance'] = data.get('balance', '2')
        card['currency'] = data.get('currency', 'USD')
        card['source'] = data.get('source', 'kardiz')
        card_list.append(card)

    return card_list


if __name__ == "__main__":
    from ipdb import set_trace
    set_trace()

    start_id = gen_start_id()
    plan_list = get_data_list_from_tsv('./logs/in/credit_card.txt', start_id)
    # email_plan_map = {data['used_by']: data for data in plan_list}

    email_plan_map = {}
    for data in plan_list:
        email = data['used_by']
        if email not in email_plan_map:
            email_plan_map[email] = data
            continue
        plan = email_plan_map[email]
        if plan['asin'] != data['asin'] or plan['keywords'] != data[keywords]:
            plan['asin'] = '%s\t%s' % (plan['asin'], data['asin'])
            plan['keywords'] = '%s\t%s' % (plan['keywords'], data['keywords'])
            plan['brand'] = '%s\t%s' % (plan.get('brand', 'King Love'),
                                        data.get('brand', 'King Love'))
            plan['gift_card'] = '%s\t%s' % (plan.get('gift_card', ''),
                                            data.get('gift_card', ''))
            # promotion
            new_promo = data.get('promotion', '')
            old_promo = plan.get('promotion', '')
            if new_promo and new_promo in old_promo:
                new_promo = ''
            plan['promotion'] = '%s\t%s' % (
                old_promo, new_promo if new_promo not in old_promo else '')

    lines = ''
    with io.open('./conf/order_address.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()
    order_addr_map = json.loads(lines)

    lines = ''
    with io.open('./logs/in/account.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()
    account_list = json.loads(lines)

    card_list = get_card_list(plan_list)

    for account in account_list:
        email = account['email']
        if email not in email_plan_map:
            continue

        plan = email_plan_map[email]
        order_num = plan['order_num']
        account['addr_id'] = order_addr_map[order_num]['id']
        account['asin'] = plan['asin']
        account['keywords'] = plan['keywords']
        account['brand'] = plan.get('brand', 'King Love')
        account['gift_card'] = plan.get('gift_card', '')
        account['promotion'] = plan.get('promotion', '')
        account['card_number'] = plan.get('card_number', '')
        account['valid_period'] = plan.get('valid_period', '')
        account['CVV'] = plan.get('CVV', '')

    with io.open('./logs/out/account.json', 'w+',
                 encoding='utf-8') as fp:
        lines = json.dumps(account_list, indent=2, ensure_ascii=False,
                           encoding='utf8')
        fp.write(lines)
