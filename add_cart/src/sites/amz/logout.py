from __future__ import absolute_import

from .amz_base import AmzBase


class Logout(AmzBase):
    url_tmpl = 'https://{market}/gp/flex/sign-out.html/' +\
        'ref=nav_youraccount_signout?ie=UTF8&action=sign-out' +\
        '&path=%2Fgp%2Fyourstore%2Fhome&signIn=1&useRedirectOnSuccess=1'

    def __init__(self, driver, params):
        AmzBase.__init__(self, driver, params)
        self.url = self.url_tmpl.format(**{'market': self.url})

    def navigate(self):
        self.driver.get(self.url)
        return True
