# -*- coding: utf-8 -*-
import sys
import json
# from pprint import pprint

reload(sys)
sys.setdefaultencoding('utf8')


class ProxyConf(object):

    def __init__(self, country, port):
        self.country = country
        self.port = port
        self.ips = []
        self.keep_alive = 30
        self.max_requests = 0
        self.pool_size = 0
        self.seed = False
        self.session = True
        self.session_duration = 0
        self.session_random = True
        self.whitelist_ips = []
        self.zone = 'gen'


if __name__ == '__main__':
    # from ipdb import set_trace
    # set_trace()

    # proxy = ProxyConf('de', 24000)
    # pprint(proxy)
    all_conf = {
        '_defaults': {
            'customer': 'aceec',
            'password': 'f0cedf3bdb2e'
            },
        'proxies': [
            ]
    }

    for i in xrange(100, 200):
        all_conf['proxies'].append(ProxyConf('de', 24000 + i).__dict__)

    for i in xrange(1, 21):
        all_conf['proxies'].append(ProxyConf('ca', 25000 + i).__dict__)

    lines = json.dumps(all_conf, indent=2)
    with open('./logs/out/proxy.conf', 'w+') as fp:
        fp.write(lines)
