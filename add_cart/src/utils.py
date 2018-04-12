# -*- coding: utf-8 -*-
from __future__ import absolute_import
import threading
import types
import time
import logging as log
from datetime import datetime, timedelta
from functools import wraps
import re
from random import uniform, choice, randint
from urllib import quote_plus


anonymous = {'None detected': 1, 'Suspected network sharing device': 2,
             'Network sharing device or proxy server': 3,
             'Suspected proxy server': 4,
             'Confirmed proxy server': 5, 'Open proxy server': 6}

level_list = {'elite proxy': 1, 'elite': 1, 'Anonymous': 2, 'transparent': 3,
              'anonymous': 2}

country_month_map = {3: {'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
                         'April': 'April', 'May': 'May', 'Jun': 'June',
                         'July': 'July', 'Aug': 'August', 'Sept': 'September',
                         'Oct': 'October', 'Nov': 'November',
                         'Dec': 'December'},
                     4: {'Januar': 'January', 'Februar': 'February',
                         'März': 'March',
                         'April': 'April', 'Mai': 'May', 'Juni': 'June',
                         'Juil': 'July', 'August': 'August',
                         'September': 'September',
                         'Oktober': 'October', 'November': 'November',
                         'Dezember': 'December'},
                     5: {'janvier': 'January', 'février': 'February',
                         'mars': 'March',
                         'avril': 'April', 'mai': 'May', 'juin': 'June',
                         'juillet': 'July', 'août': 'August',
                         'septembre': 'September',
                         'octobre': 'October', 'novembre': 'November',
                         'décembre': 'December'},
                     7: {'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
                         'April': 'April', 'May': 'May', 'Jun': 'June',
                         'July': 'July', 'Aug': 'August', 'Sept': 'September',
                         'Oct': 'October', 'Nov': 'November',
                         'Dec': 'December'},
                     44551: {'de enero de': 'January',
                             'de febrero de': 'February',
                             'de marzo de': 'March',
                             'de abril de': 'April', 'de mayo de': 'May',
                             'de junio de': 'June',
                             'de julio de': 'July', 'de agosto de': 'August',
                             'de septiembre de': 'September',
                             'de octubre de': 'October',
                             'de noviembre de': 'November',
                             'de diciembre de': 'December'},
                     35691: {'gennaio': 'January', 'febbraio': 'February',
                             'marzo': 'March',
                             'aprile': 'April', 'maggio': 'May',
                             'giugno': 'June',
                             'luglio': 'July', 'agosto': 'August',
                             'settembre': 'September',
                             'ottobre': 'October', 'novembre': 'November',
                             'dicembre': 'December'},
                     1: {'January': 'January', 'February': 'February',
                         'March': 'March',
                         'April': 'April', 'May': 'May', 'June': 'June',
                         'July': 'July', 'August': 'August',
                         'September': 'September',
                         'October': 'October', 'November': 'November',
                         'December': 'December'},
                     }

country_re_map = {1: '%B %d, %Y', 3: '%d %B %Y', 4: '%d. %B %Y',
                  5: '%d %B %Y', 7: '%B %d %Y', 44551: '%d %B %Y',
                  35691: '%d %B %Y'}

MARKETPLACE_MAP = {
    1: 'www.amazon.com',
    3: 'www.amazon.co.uk',
    4: 'www.amazon.de',
    5: 'www.amazon.fr',
    6: 'www.amazon.co.jp',
    7: 'www.amazon.ca',
    44551: 'www.amazon.es',
    35691: 'www.amazon.it'}


class Object(object):
    pass


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def dict2object(dic):
    '''
    convert dict to object, key become attr of the object.
    recursive.
    '''
    if not isinstance(dic, dict):
        return dic
    ret = Object()
    for k, v in dic.iteritems():
        ret.__dict__[k] = dict2object(v)
    return ret

# Now I know amazon has three type of product url
# 1.http://www.amazon.com/dp/B00UOEAN40
# 2.https://www.amazon.com/gp/product/B01DIOTF46
# 3.http://www.amazon.com/Apple-Macbook-Case-Inch-Snugg/dp/B00DN6TSVA
# It will have bug in the fucture because I don't know whether how the
# types will change.


def from_url_get_asin(url):
    url = url.lower()
    split_url = url.split('/')
    i = -1
    asin = None
    for idx, s in enumerate(split_url):
        if 'amazon' in s:
            i = idx
            break
    if i == -1:
        return None
    try:
        if split_url[i+1] == 'dp':
            asin = split_url[i+2][:10]
        elif split_url[i+1] == 'gp' and split_url[i+2] == 'product':
            asin = split_url[i+3][:10]
        elif split_url[i+2] == 'dp':
            asin = split_url[i+3][:10]
        return asin.upper() if asin else None
    except Exception:
        return None


def format_translation(ladder):
    ladder_split = ladder.encode('utf-8').replace('&', ' ').split(' ')
    final_list = []
    for ls in ladder_split:
        if ls:
            final_list.append(ls)
    return final_list


def format_group(group):
    new_group = group.lower().replace(' & ', '_').split(',')
    group_list = []
    for ng in new_group:
        group_list.append(ng.replace('(',
                          '').replace(')', '').strip().replace(' ', '_'))
    return '(%s)' % ','.join(group_list)


# in order to format ecsp_amz_us_group_map value to
# amz_search_engine_summary SQL (WHERE IN)
# eg: "('Health & Personal Care', \n      'Personal_Care_Appliances')"
#   format to "('Health & Personal Care','Personal_Care_Appliances')"
# use functons: dispatch_channel
def group_strip(group):
    group_list = []
    for ng in group.split(','):
        group_list.append(ng.strip())
    return ','.join(group_list)


# in order to format best seller category  to ecsp_amz_us_group_map key
# eg: 'Health & Personal Care'  format to 'health_personal_care'
# use functions: get_seller_ranks
def format_to_group_map(ladder):
    return ladder.replace(' & ', '_').replace(', ', '_').replace(' ', '_').\
        lower()


# in order to format best seller category to rank_keywords arg
# eg: 'Health & Personal Care' format to ['health', 'personal', 'care']
# use function: GetMarketplaceList
def category_format_to_arg(ladder_list):
    new_ladder_list = []
    for ladder in ladder_list:
        ladder = ladder.replace(' & ', ' ').replace(', ', ' ').split(' ')
        new_ladder_list += ladder
    return new_ladder_list


class Sync:

    _locks = {}

    @classmethod
    def sync(cls, arg):
        lock_for_sync = threading.Lock()

        def actual_sync(func):
            lock = None
            with lock_for_sync:
                if arg not in cls._locks:
                    cls._locks[arg] = threading.RLock()
                lock = cls._locks[arg]

            def wrapper(*args, **kwargs):
                with lock:
                    return func(*args, **kwargs)

            return wrapper

        return actual_sync


class Singleton(type):
    _instances = {}

    @Sync.sync(__name__)
    def __call__(cls, *args, **kwargs):
        # Add @Sync.sync decorator to make it thread safe but with some more
        # efforts, so it is better store an instance as a variable and keep
        # using that variable

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


def merge_dict(dict1, dict2):
    for k, v in dict2.iteritems():
        if k in dict1:
            if isinstance(dict1[k], types.DictType) and\
                    isinstance(v, types.DictType):
                new_data = merge_dict(dict1[k], v)
                if not new_data:
                    return None
                dict1[k] = new_data
            elif isinstance(dict1[k], types.ListType) and\
                    isinstance(v, types.ListType):
                # XXX: TODO - Need to remove the duplicated data
                dict1[k].extends(v)
            elif dict1[k] == v:
                pass
            else:
                return None
        else:
            dict1[k] = v

    return dict1


def compare_dict(d1, d2):
    '''
this method id copy from
http://stackoverflow.com/questions/4527942/comparing-two-dictionaries-in-python
    '''
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())

    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys

    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])

    return added, removed, modified, same


def get_score(timeused):
    return int(100 - timeused)


class Proxyip:
    def __init__(self, ip, port, type, username=None, password=None):
        self.ip = ip
        self.port = port
        self.type = type
        self.username = username
        self.password = password
        self.create_at = time.time()

    def __repr__(self):
        if not self.username:
            return r'%s://%s:%s' % (self.type.lower(), self.ip, self.port)
        else:
            return r'%s://%s:%s@%s:%s' % (self.type.lower(), self.username,
                                          self.password, self.ip, self.port)


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        try:
            result = method(*args, **kw)
        finally:
            te = time.time()
            log.info('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw,
                                                te-ts))
        return result

    return timed


def json_decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = json_decode_list(item)
        elif isinstance(item, dict):
            item = json_decode_dict(item)
        rv.append(item)
    return rv


def json_decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = json_decode_list(value)
        elif isinstance(value, dict):
            value = json_decode_dict(value)
        rv[key] = value
    return rv


def make_last_month_period(dt=None):
    """
    input a datetime instance return an int
    """
    if not dt:
        dt = datetime.utcnow()
    dt = dt.replace(day=1) - timedelta(days=1)
    return dt.strftime('%Y%m')


def make_last_year_month_period(dt=None):
    """
    input a datetime instance return an int
    """
    if not dt:
        dt = datetime.utcnow()
    dt = dt.replace(year=dt.year - 1, month=dt.month, day=1)
    return int(dt.strftime('%Y%m'))


def make_month_before_last_month_period(return_list=False):
    dt = datetime.utcnow().replace(day=1) - timedelta(days=1)
    if return_list:
        month_list = [str(make_last_month_period(dt)),
                      str(make_last_year_month_period(dt))]
        return month_list
    else:
        return make_last_month_period(dt)


def time_gap(time_delta):
    def input_time(func):
        @wraps(func)
        def time_func(*args):
            old_time = time.time()
            result = func(*args)
            now = time.time()
            delta = now - old_time
            value = time_delta() if hasattr(time_delta, '__call__') \
                else time_delta
            if delta < value:
                time.sleep(value - delta)
            return result
        return time_func
    return input_time


def make_amz_product_url(website, canonical, asin, merchant_id='',
                         assoc_tag=''):
    canonical_part = '' if not canonical else '/%s' % canonical
    merchant_part = '' if not merchant_id else '&m=%s&ref_=v_sp_detail_page'\
        % merchant_id
    tag_part = '' if not assoc_tag else '&tag=%s' % assoc_tag
    _tmpl = 'https://{website}{canonical}/dp/{asin}?ie=UTF8{tag}{merchant}'

    return _tmpl.format(**{'website': website,
                           'canonical': canonical_part, 'asin': asin,
                           'merchant': merchant_part,
                           'tag': tag_part})


class Discount:
    PERCENTAGE_TYPE = 1
    FLAT_TYPE = 2

    def __init__(self, price, discount, discount_type):
        self.price = price
        self.discount = discount
        self.discount_type = discount_type

    def get_final_price(self):
        def _get_percentage_price(p, v):
            return round(p * (100.0 - v) / 100, 2)

        def _get_flat_price(p, v):
            return round(p - v, 2)

        if self.discount_type == self.PERCENTAGE_TYPE:
            return _get_percentage_price(self.price, self.discount)

        if self.discount_type == self.FLAT_TYPE:
            return _get_flat_price(self.price, self.discount)


def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)


def get_datetime_from_string(string, market):
    p = re.compile('(\D+)')
    try:
        for token in p.findall(string):
            token = token.strip()
            if not token:
                continue

            data = token.replace('.', '').replace(',', '').strip()
            return datetime.\
                strptime(string.replace(data, country_month_map[market][data]),
                         country_re_map[market])
        else:
            return datetime.today()
    except Exception:
        return datetime.today()


class Probability:
    @classmethod
    def more_than(cls, value):
        return not cls.not_more_than(value)

    @classmethod
    def less_than(cls, value):
        return uniform(0, 100) < value

    @classmethod
    def not_less_than(cls, value):
        return not cls.less_than(value)

    @classmethod
    def not_more_than(cls, value):
        return uniform(0, 100) <= value


class ImprPrjData:
    def __init__(self, market, asin, keywords, quantity):
        self.marketplace_id = market
        self.asin = asin
        self.keywords = keywords
        self.quantity = quantity


def get_asin_target_url(url_type, asin_data):

    def _get_asin_target_url_0(asin_data):
        res = u'https://' + MARKETPLACE_MAP[asin_data['market']] + \
            '/s/ref=nb_sb_noss?url=search-alias%3D' +\
            asin_data['group_desc'] + '&field-keywords=' +\
            quote_plus(str(asin_data['keywords']))
        if asin_data['group_desc'] == 'hpc':
            res += '&fap=1'

        return res

    def _get_asin_target_url_1(asin_data):
        res = u'https://' + MARKETPLACE_MAP[asin_data['market']] + \
            '/s/ref=nb_sb_noss?url=search-alias%3D' +\
            asin_data['group_desc'] + '&field-keywords=' +\
            quote_plus(str(asin_data['keywords'])) + '&field-brandtextbin=' +\
            quote_plus(str(asin_data['brand']))
        if asin_data['group_desc'] == 'hpc':
            res += '&fap=1'

        return res

    def _get_asin_target_url_2(asin_data):
        res = u'https://' + MARKETPLACE_MAP[asin_data['market']] + \
            '/s/ref=sr_nr_p_89_0?rh=%s&keywords=%s' % (
                quote_plus('i:%s,k:%s,p_89:%s' % (
                    asin_data['group_desc'], quote_plus(asin_data['keywords']),
                    quote_plus(asin_data['brand']))),
                quote_plus(asin_data['keywords']))
        if asin_data['group_desc'] == 'hpc':
            res += '&fap=1'

        return res

    def _get_asin_target_url_3(asin_data):
        return asin_data.get('url', '')

    def _get_asin_target_url_4(asin_data):
        if asin_data['group_desc'] == 'hpc':
            return _get_asin_target_url_1(asin_data)

        return u'https://' + MARKETPLACE_MAP[asin_data['market']] + \
            '/s/ref=sr_nr_p_36_0?' +\
            'field-keywords=' + quote_plus(str(asin_data['keywords'])) +\
            '&field-brandtextbin=' + quote_plus(str(asin_data['brand']))

    if url_type == 0:
        return _get_asin_target_url_0(asin_data)
    elif url_type == 1:
        return _get_asin_target_url_1(asin_data)
    elif url_type == 2:
        return _get_asin_target_url_2(asin_data)
    elif url_type == 3:
        return _get_asin_target_url_3(asin_data)
    else:
        return _get_asin_target_url_4(asin_data)


def make_date_period(dt=None):
    """
    input a datetime instance return an int
    """
    if not dt:
        dt = datetime.utcnow()
    return int(dt.strftime('%Y%m%d'))


def format_telephone(phone):
    phone = ''.join(re.findall('\d', phone))
    if phone.startswith('049'):
        return phone

    if len(phone) == 10:
        phone = '01' + phone
    elif len(phone) == 11:
        phone = '0' + phone
    elif len(phone) != 12:
        return ''

    return phone


def gen_us_telephone(area_code=None, area_name=None):
    _area_code_map = {
        'Alaska': [907],
        'Alabama': [205, 251, 256, 334],
        'Arkansas': [479, 501, 870],
        'Arizona': [480, 520, 602, 623, 928],
        'California': [209, 213, 310, 323, 408, 415, 510, 530, 559, 562, 619,
                       626, 650, 661, 707, 714, 760, 805, 818, 831, 858, 909,
                       916, 925, 949, 951],
        'Colorado': [303, 719, 970],
        'Connecticut': [203, 860],
        'District of Columbia': [202],
        'Delaware': [302],
        'Florida': [239, 305, 321, 352, 386, 407, 561, 727, 772, 813, 850, 863,
                    904, 941, 954],
        'Georgia': [229, 404, 478, 706, 770, 912],
        'Hawaii': [808],
        'Iowa': [319, 515, 563, 641, 712],
        'Idaho': [208],
        'Illinois': [217, 309, 312, 618, 630, 708, 773, 815, 847],
        'Indiana': [219, 260, 317, 574, 765, 812],
        'Kansas': [316, 620, 785, 913],
        'Kentucky': [270, 502, 606, 859],
        'Louisiana': [225, 318, 337, 504, 985],
        'Massachusetts': [413, 508, 617, 781, 978],
        'Maryland': [301, 410],
        'Maine': [207],
        'Michigan': [231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 989],
        'Minnesota': [218, 320, 507, 612, 651, 763, 952],
        'Missouri': [314, 417, 573, 636, 660, 816],
        'Mississippi': [228, 601, 662],
        'Montana': [406],
        'North Carolina': [252, 336, 704, 828, 910, 919],
        'North Dakota': [701],
        'Nebraska': [308, 402],
        'New Hampshire': [603],
        'New Jersey': [201, 609, 732, 856, 908, 973],
        'New Mexico': [505, 575],
        'Nevada': [702, 775],
        'New York': [212, 315, 516, 518, 585, 607, 631, 716, 718, 845, 914],
        'Ohio': [216, 330, 419, 440, 513, 614, 740, 937],
        'Oklahoma': [405, 580, 918],
        'Oregon': [503, 541],
        'Pennsylvania': [215, 412, 570, 610, 717, 724, 814],
        'Rhode Island': [401],
        'South Carolina': [803, 843, 864],
        'South Dakota': [605],
        'Tennessee': [423, 615, 731, 865, 901, 931],
        'Texas': [210, 214, 254, 281, 325, 361, 409, 432, 512, 713, 806, 817,
                  830, 903, 915, 936, 940, 956, 972, 979],
        'Utah': [435, 801],
        'Virginia': [276, 434, 540, 703, 757, 804],
        'Vermont': [802],
        'Washington': [206, 253, 360, 425, 509],
        'Wisconsin': [262, 414, 608, 715, 920],
        'West Virginia': [304],
        'Wyoming': [307],
    }

    all_area_codes = []
    for area_codes in _area_code_map.values():
        all_area_codes += area_codes

    if not area_code or area_code not in _area_code_map.values:
        if not area_name or area_name not in _area_code_map:
            area_name = choice(_area_code_map.keys())
        area_code = choice(_area_code_map[area_name])
    return '%s-%03d-%04d' % (area_code, randint(001, 999), randint(0001, 9999))


def get_balance(balance_text):
    try:
        return int(''.join(re.findall('\d', balance_text)))
    except Exception:
        return 0


def gen_start_id():
    return make_date_period() * 1000
