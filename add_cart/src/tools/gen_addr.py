# -*- coding: utf-8 -*-
import sys
import io
import json
from random import randint
from collections import OrderedDict
from utils import format_telephone, gen_start_id

reload(sys)
sys.setdefaultencoding('utf8')


def get_data_list_from_tsv(file_name, start_id):
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

        if start_id:
            data['id'] = start_id + i - 1

        data_list.append(data)

    return data_list


if __name__ == "__main__":
    from ipdb import set_trace
    set_trace()

    card_prepare_list = []

    start_id = gen_start_id()
    card_prepare_list = get_data_list_from_tsv(
        './logs/in/credit_card_prepare.txt', start_id)

    lines = ''
    with io.open('./conf/order_address.json', 'r', encoding='utf-8') as fp:
        lines = fp.read()
    order_addr_map = json.loads(lines)

    from datetime import datetime, timedelta
    start_time = datetime.now()

    for card in card_prepare_list:
        addr = order_addr_map[card['order_num']]
        card['telephone'] = format_telephone(card['telephone'])
        card['address_line1'] = addr['address_line1']
        card['address_line2'] = addr['address_line2']
        card['city'] = addr['city']
        card['zip_code'] = addr['zip_code']
        card['state'] = addr['state']
        card['country'] = addr['country']
        card['used_at'] = ''
        card['source'] = 'kardiz'

        val = randint(20 * 365, 50 * 365)
        dt = start_time - timedelta(days=val)
        card['birthday'] = dt.strftime('%Y-%m-%d')

    headers = ['email', 'password', 'given_name', 'surname', 'telephone',
               'binded_email', 'binded_passwd', 'order_num', 'test_by',
               'test_result', 'test_date', 'comments', 'card_number',
               'expired_date', 'CVV', 'used_at', 'source', 'birthday',
               'address_line1', 'address_line2', 'city', 'state', 'zip_code',
               'country']
    # from ipdb import set_trace
    # set_trace()
    out_file = './logs/out/credit_card_prepare.txt'
    with io.open(out_file, 'w+', encoding='utf-8') as fp:
        line = '\t'.join(headers)
        lines = [unicode(line + '\n')]
        for card in card_prepare_list:
            values = [card.get(header, '') for header in headers]
            line = '\t'.join(values)
            lines.append(unicode(line + '\n'))
        fp.writelines(lines)
