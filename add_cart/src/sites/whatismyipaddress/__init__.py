from __future__ import absolute_import

import os
from .home import Home


def test_ip(driver, account, params):
    if 'debug_with_image' in params:
        image_folder = '%s/image/test_ip' % (os.getcwd())
        if not os.path.isdir(image_folder):
            os.makedirs(image_folder)

    home = Home(driver, params)
    home.navigate()

    if 'debug_with_image' in params:
        driver.save_screenshot('%s/screen_%s.png' % (image_folder,
                                                     account.get('email')))
