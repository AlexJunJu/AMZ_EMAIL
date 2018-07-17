# -*- coding: utf-8 -*-
import sys
import io
import json
import random
# import logging as log
# from iso_country_codes import get_country
from collections import OrderedDict
from model import MlaProfile
from utils import format_telephone, gen_us_telephone, gen_start_id

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


def load_accounts(all_data_list):
    account_list = []
    for i in xrange(len(all_data_list)):
        acct = OrderedDict()
        card = all_data_list[i]
        acct['market_place_id'] = 4
        acct['id'] = card.get('id', '')
        acct['email'] = card.get('email', '')
        acct['password'] = card.get('password', '')
        acct['given_name'] = card.get('given_name', '')
        acct['surname'] = card.get('surname', '')
        acct['telephone'] = card.get('telephone', '')
        acct['order_num'] = card.get('order_num', '')
        acct['asin'] = card.get('asin', '')
        acct['keywords'] = card.get('keywords', '')
        acct['price'] = card.get('price', '')
        acct['gift_card'] = card.get('gift_card', '')
        account_list.append(acct)

    return account_list


def bind_addr_to_acct(account_list, addr_map):
    for account in account_list:
        account['addr_id'] = addr_map[account['order_num']]['id']


def bind_profile_to_acct(account_list, profile_list, country):
    profile_list = [p for p in profile_list if p.country == country]
    index = [random.randint(0, len(profile_list))]

    def _get_profile():
        if index[0] >= len(profile_list):
            index[0] = 0
        profile_id = profile_list[index[0]].profile_id
        name = profile_list[index[0]].name
        index[0] += 1
        return profile_id, name

    for acct in account_list:
        acct['mla_profile'], acct['mla_profile_name'] = _get_profile()


def load_order_address_from_tsv(file_name):
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        return json.loads(fp.read())


def load_cards(all_data_list):
    card_list = []
    for data in all_data_list:
        card = OrderedDict()
        card['id'] = data['id']
        card['email'] = data['binded_email']
        card['source'] = data['source']
        card['password'] = data['binded_passwd']
        card['card_holder'] = '%s %s' % (data['given_name'], data['surname'])
        card['card_number'] = data['card_number']
        card['expired_date'] = data['valid_period']
        card['telephone'] = data['telephone']
        if len(card['expired_date']) == len('08-20'):
            tokens = str(card['expired_date']).split('-')
            card['expired_date'] = '20%s-%s-01' % (tokens[1], tokens[0])
        card['balance'] = '12.5'  # hard code
        card['currency'] = 'USD'  # hard code
        card['is_used'] = True
        card['used_by_email'] = data['used_by']
        card['order_num'] = data['order_num']

        card_list.append(card)

    return card_list


if __name__ == "__main__":
    from ipdb import set_trace
    set_trace()

    start_id = gen_start_id() + 200
    all_data_list = get_data_list_from_tsv('./logs/in/credit_card_prepare.txt',
                                           start_id=start_id)
    for i in xrange(len(all_data_list)):
        card = all_data_list[i]
        telephone = card.get('telephone', '')
        if not telephone:
            telephone = gen_us_telephone()
        card['telephone'] = format_telephone(telephone)

    account_list = load_accounts(all_data_list)
    lines = '[]'
    with io.open('./conf/account.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()
    old_account_list = json.loads(lines)
    old_account_by_email = {acct['email']: acct for acct in old_account_list}

    valid_acct_list = []
    for acct in account_list:
        if acct['email'] in old_account_by_email:
            print '%s is invalid' % acct['email']
            continue
        valid_acct_list.append(acct)

    account_list = valid_acct_list
    account_by_email = {acct['email']: acct for acct in account_list}

    country = 'de'
    profile_list = load_profiles()
    bind_profile_to_acct(account_list, profile_list, country)

    with io.open('./logs/out/account.json', 'w+', encoding='utf-8') as fp:
        lines = json.dumps(account_list, indent=2, ensure_ascii=False,
                           encoding='utf8')
        fp.write(unicode(lines))

    headers = ['email', 'password', 'given_name', 'surname', 'telephone',
               'binded_email', 'binded_passwd']
    out_files = './logs/out/credit_card_prepare.txt'
    with io.open(out_files, 'w+', encoding='utf-8') as fp:
        line = '\t'.join(headers)
        lines = [unicode(line + '\n')]
        for data in all_data_list:
            values = [data.get(header, '') for header in headers]
            line = '\t'.join(values)
            lines.append(unicode(line + '\n'))
        fp.writelines(lines)
