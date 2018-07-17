# -*- coding: utf-8 -*-
import sys
import io
import json
import time
from datetime import datetime
from iso_country_codes import get_country
from collections import OrderedDict
from mws_utils import make_mws_api

reload(sys)
sys.setdefaultencoding('utf8')


def get_order_list(file_name, start, end):
    lines = None
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    order_list = []
    for i in xrange(1, len(lines)):
        tokens = lines[i].split('\t')
        yr_date = tokens[2].strip()
        order_num = tokens[4].strip()
        if start and yr_date < start:
            continue
        if end and yr_date >= end:
            continue
        order_list.append(order_num)

    return order_list


def get_data_list_from_tsv(file_name):
    lines = None
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    data_list = []
    headers = [col.strip() for col in lines[0].split('\t')]

    for i in xrange(1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        data = OrderedDict()
        tokens = line.split('\t')
        for j in xrange(len(headers)):
            data[headers[j]] = tokens[j] if j < len(tokens) else ''

        data_list.append(data)

    return data_list


def gen_address_list(order_num_list):
    api = make_mws_api(4, 'KingLove')
    order_info_list = api.get_orders(order_num_list)

    data_list = OrderedDict()
    for i in xrange(len(order_info_list)):
        addr = order_info_list[i].ShippingAddress
        if not hasattr(addr, 'PostalCode'):
            print 'ERROR: not PostalCode, %s ' % addr
            continue

        data = OrderedDict()

        tokens = addr.Name.split(' ')
        data['given_name'] = tokens[0]
        data['surname'] = ''.join(tokens[1:])

        data['address_line1'] = \
            addr.AddressLine1 if hasattr(addr, 'AddressLine1') else ''
        data['address_line2'] = \
            addr.AddressLine2 if hasattr(addr, 'AddressLine2') else ''

        data['city'] = addr.City

        data['zip_code'] = addr.PostalCode
        data['state'] = \
            addr.StateOrRegion if hasattr(addr, 'StateOrRegion') else ''
        data['country'] = get_country(addr.CountryCode)
        data['telephone'] = ''
        data['gate_code'] = ''
        data_list[order_info_list[i].AmazonOrderId] = data

    return data_list


def _chunks(data_list, n):
    for i in xrange(0, len(data_list), n):
        yield data_list[i:i+n]


if __name__ == "__main__":
    from ipdb import set_trace
    set_trace()

    data_list = get_data_list_from_tsv(
        './logs/in/all_de_FBA_express_orders.txt')

    def _filter(data):
        yr_date = int(data.get('yr_date', 0))
        return yr_date >= 20170501 and yr_date < 20170701

    order_num_list = [data['amazon_order_id'] for data in data_list
                      if _filter(data)]
    set_trace()
    order_map = OrderedDict()

    i = 0
    for order_nums in _chunks(order_num_list, 50):
        print '[%s]start to fetch %04d ' % (datetime.now(), i)
        result = gen_address_list(order_nums)
        order_map.update(result)
        i += 1
        time.sleep(60)

    start_id = 400001
    addr_list = order_map.values()
    for i in xrange(len(addr_list)):
        addr = addr_list[i]
        addr['id'] = start_id + i

    with io.open('./logs/out/address.json', 'w+',
                 encoding='utf-8') as fp:
        lines = json.dumps(addr_list, indent=2, ensure_ascii=False,
                           encoding='utf8')
        fp.write(lines)

    with io.open('./logs/out/order_address.json', 'w+',
                 encoding='utf-8') as fp:
        lines = json.dumps(order_map, indent=2, ensure_ascii=False,
                           encoding='utf8')
        fp.write(lines)
