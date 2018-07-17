from __future__ import absolute_import

import time
import random
from .amz_base import AmzBase


class ExitNode(AmzBase):

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)

    def is_done(self):
        return True

    def navigate(self):
        exit_node = self.params.get('exit_node')
        if not exit_node:
            return False

        url = 'http://{market}/dp/{asin}'.format(**{'market': self.url,
                                                    'asin': exit_node})
        self.driver.get(url)
        time.sleep(3 + random.randint(1, 3))
        return True

    def process(self):
        pass


class EntryNode(ExitNode):

    def __init__(self, driver, params):
        ExitNode.__init__(self, driver, params)

    def navigate(self):
        entry_node = self.params.get('entry_node')
        if not entry_node:
            return False

        url = 'http://{market}/dp/{asin}'.format(**{'market': self.url,
                                                    'asin': entry_node})
        self.driver.get(url)
        time.sleep(3 + random.randint(1, 3))
        return True
