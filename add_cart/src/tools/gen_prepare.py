# -*- coding: utf-8 -*-
import sys
import io
import json
import random
# import logging as log
# from iso_country_codes import get_country
from collections import OrderedDict
from model import MlaProfile
from utils import format_telephone

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
        try:
            for j in xrange(len(headers)):
                data[headers[j]] = tokens[j]
        except Exception:
            print 'ERROR: %s' % line
            continue

        if start_id:
            data['id'] = start_id + i - 1

        data_list.append(data)

    return data_list

if __name__ == "__main__":
    from ipdb import set_trace
    set_trace()

    start_id = 201000
    order_account_list = get_data_list_from_tsv('./logs/in/order_account.txt',
                                                start_id=start_id)
    account_list = get_data_list_from_tsv('./logs/in/account_db.txt',
                                           start_id=start_id)

    wish_list = get_data_list_from_tsv('./logs/in/wish_account.txt',
                                       start_id=start_id)
    wish_map = {data['email'] : data for data in wish_list}

    not_in_wish_list = []
    no_binded_email = []
    new_account_list = []
    for account in account_list:
        wish_account = wish_map.get(account['email'])
        if not wish_account:
            # print '%s is not in wish_account' % account['email']
            not_in_wish_list.append(account['email'])
            continue
        if not wish_account.get('binded_email'):
            print '%s has not binded_email' % account['email']
            no_binded_list.append(account['email'])
            continue

        account['binded_email'] = wish_account['binded_email']
        account['binded_passwd'] = wish_account['binded_email_passwd']
        account['telephone'] = format_telephone(account['telephone'])
        new_account_list.append(account)

    not_in_new_account_map = []
    new_account_map = {data['email'] : data for data in new_account_list}
    print '\n\n\n\n\n'
    headers = ['email', 'password', 'given_name', 'surname', 'telephone',
               'binded_email', 'binded_passwd', 'order_num']
    out_file = './logs/out/credit_card_prepare.txt'
    with io.open(out_file, 'w+', encoding='utf-8') as fp:
        line = '\t'.join(headers)
        lines = [unicode(line + '\n')]
        for order_acct in order_account_list:
            account = new_account_map.get(order_acct['email'])
            if not account:
                # print '%s is not in new_account_map' % order_acct['email']
                not_in_new_account_map.append(order_acct['email'])
                continue
            values = [account.get(header, '') for header in headers]
            line = '\t'.join(values)
            lines.append(unicode(line + '\n'))
        fp.writelines(lines)

    set_trace()
    set_trace()
    set_trace()
    set_trace()
    set_trace()
