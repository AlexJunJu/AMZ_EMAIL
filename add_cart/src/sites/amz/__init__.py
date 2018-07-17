from __future__ import absolute_import

from .home import Home
from .signin import SigninWithCaptcha
from .register import RegisterWithCaptcha
from .logout import Logout
from .bind_credit_card import BindCreditCard
from .prime import EnablePrime, DisablePrime, PrimeStep
from .amz_confirm_adult import ConfirmAdult
from .search import SearchAndGotoAsin
from .add_to_cart import AddToCart
from .clear_cart import ClearCart
from .checkout_cart import CheckoutCart
from .place_order import PlaceOrder
from .gift_card import BuyGiftCard, CheckGiftCard, RedeemGiftCard
from .add_addr import AddAddress
from .exit_node import ExitNode, EntryNode
from sites.exception import (StepFailed, CaptchaException, FailedToRegNewUser,
                             MeetSpammedAccount)
import os
import logging as log
import time
import random
from datetime import datetime
from model import (AmzMarketplace)


def _gen_log(driver, account, params):
    def _do_log(step, msg, is_exception=False):
        if is_exception:
            log.exception('<%s>:<%s>, %s' % (datetime.utcnow(), step, msg))
        else:
            log.info('<%s>:<%s>, %s' % (datetime.utcnow(), step, msg))

    if 'debug_with_image' not in params:
        return _do_log

    image_folder = '%s/image/%s' % (os.getcwd(), account.get('email'))
    if not os.path.isdir(image_folder):
        os.makedirs(image_folder)

    def _do_log_with_image(step, msg, is_exception=False):
        _do_log(step, msg, is_exception)
        driver.save_screenshot('%s/01_%s.png' % (image_folder, step))

    return _do_log_with_image


def _common_process(driver, account, params, prepare, process):
    _log = _gen_log(driver, account, params)

    if prepare and not prepare(params):
        return False

    try:
        # home
        home = Home(driver, params)
        home.navigate()
        _log('home', account.get('email'))
        if not home.is_done():
            raise StepFailed('Failed to visit home')

        # signinlog.exception('
        signin = SigninWithCaptcha(driver, params, account)
        signin.navigate()
        signin.process()
        _log('signin', '')
        # if not signin.signin.is_done():
        # if signin.is_auth_err():
        if signin.is_new_account():
            # Maybe we don't meet all status, so is_done can't work.
            reg = RegisterWithCaptcha(driver, params, account)
            reg.navigate()
            reg.process()
            _log('register', '')
            if not reg.is_done():
                raise FailedToRegNewUser('Failed to register new user')

        if process:
            process(driver, account, params)

        # logout
        logout = Logout(driver, params)
        logout.navigate()
        _log('logout', account.get('email'))

        return True
    except (FailedToRegNewUser, MeetSpammedAccount) as e:
        _log('failed_to_reg_new_user', '%s' % e)
        # XXX: Need to raise the exception and move the below codes to outside
        # acct = AmzAccountInfo.get_by_market_email(
        #     params.get('market_place_id'), account.get('email'))
        # if not acct:
        #     _log('failed_to_reg_new_user_02',
        #          'account(%s, %s) not found' % (params.get('market_place_id'),
        #                                         account.get('email')))
        #     return

        # acct.soft_delete()
        # AmzFailAccountLog(account_id=acct.id,
        #                   market_place_id=acct.market_place_id,
        #                   email=acct.email).add()
    except (StepFailed, CaptchaException) as e:
        # from ipdb import set_trace
        # set_trace()
        # @TODO need to log error message to DB (AmzSaleFarmPrjTask)
        _log('exception', '%s' % e)
    except Exception as e:
        # from ipdb import set_trace
        # set_trace()
        _log('exception', '%s' % e)
        log.exception('Failed to execute %s:%s, %s, %s' %
                      (driver.name, process.__name__, account, params))
        raise e


def amz_add_address(driver, account, params):

    def _prepare(params):
        return True

    def _process(driver, account, params):
        add_addr = AddAddress(driver, params, account)
        add_addr.navigate()
        add_addr.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_add_to_cart(driver, account, params):
    _log = _gen_log(driver, account, params)

    def _prepare(params):
        if 'market_place_id' not in params:
            return False

        market_place_id = params.get('market_place_id')
        if AmzMarketplace.is_japan(market_place_id):
            # params['adult_asin_list'] = params.get('is_adult')
            params['jp_adult_asin'] = params.get('is_adult')

        return True

    def _process(driver, account, params):
        # params.get('jp_adult_asin') exist? False
        if params.get('jp_adult_asin'):
            confirm_adult = ConfirmAdult(driver, params, params['asin'])
            confirm_adult.process()

        # search and add to cart
        search = SearchAndGotoAsin(driver, params)
        search.process()
        _log('search_%s' % (params['keywords'].replace(' ', '_')), '')

        add2cart = AddToCart(driver, params, True)
        add2cart.process()
        _log('add2cart_%s_%s' % (params['keywords'].replace(' ', '_'),
                                 params['asin']), '')

    return _common_process(driver, account, params, _prepare, _process)


def amz_clear_cart(driver, account, params):
    def _prepare(params):
        return True

    def _process(driver, account, params):
        # clear cart
        cart = ClearCart(driver, params)
        cart.navigate()
        cart.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_account_register(driver, account, params):

    def _prepare(params):
        return True

    return _common_process(driver, account, params, _prepare, None)


def amz_bind_credit_card(driver, account, params):

    def _prepare(params):
        return True

    def _process(driver, account, params):
        bind_card = BindCreditCard(driver, params, account)
        if not bind_card.navigate():
            return

        bind_card.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_bind_credit_card_prime(driver, account, params):
    _log = _gen_log(driver, account, params)
    email = params.get('email')

    def _prepare(params):
        return True

    def _process(driver, account, params):
        bind_card = BindCreditCard(driver, params, account)
        if not bind_card.navigate():
            return
        bind_card.process()
        _log('bindcart_%s' % (email), '')

        time.sleep(4 + random.randint(1, 4))

        redeem_gc = RedeemGiftCard(driver, params, account)
        if redeem_gc.navigate():
            redeem_gc.process()

        time.sleep(4 + random.randint(1, 4))

        enable_prime = EnablePrime(driver, params, account)
        if not enable_prime.navigate():
            return
        enable_prime.process()
        _log('enable_prime_%s' % (email), '')

    return _common_process(driver, account, params, _prepare, _process)


def amz_enable_prime(driver, account, params):

    def _prepare(params):
        return True

    def _process(driver, account, params):
        enable_prime = EnablePrime(driver, params, account)
        if not enable_prime.navigate():
            return

        enable_prime.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_disable_prime(driver, account, params):

    def _prepare(params):
        return True

    def _process(driver, account, params):
        disable_prime = DisablePrime(driver, params, account)
        if not disable_prime.navigate():
            return

        disable_prime.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_buy_gift_cards(driver, account, params):

    def _prepare(params):
        return True

    def _process(driver, account, params):
        gift_cards = BuyGiftCard(driver, params, account)
        if not gift_cards.navigate():
            return

        gift_cards.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_create_order(driver, account, params):
    _log = _gen_log(driver, account, params)
    asin = params.get('asin')
    keywords = params.get('keywords')
    email = params.get('email')

    def _prepare(params):
        if 'market_place_id' not in params or 'asin' not in params:
            return False

        # multiple asin/keywords
        asin_list = params['asin'].split('\t')
        kw_list = params['keywords'].split('\t')
        brand_list = params['brand'].split('\t')
        promotion_list = params['promotion'].split('\t')
        gift_card_list = params['gift_card']['gift_card'].split('\t')
        if len(asin_list) != len(kw_list)\
                or len(asin_list) != len(brand_list)\
                or len(asin_list) != len(promotion_list) \
                or len(asin_list) != len(gift_card_list):
            return False

        params['asin_list'] = [data.strip() for data in asin_list]
        params['kw_list'] = [data.strip() for data in kw_list]
        params['brand_list'] = [data.strip() for data in brand_list]
        params['promotion_list'] = [data.strip() for data in promotion_list]
        params['gift_card_list'] = [data.strip() for data in gift_card_list]

        return True

    def _process(driver, account, params):
        entry_node = EntryNode(driver, params)
        if entry_node.navigate():
            entry_node.process()

        # clear cart
        clear_cart = ClearCart(driver, params)
        if clear_cart.navigate():
            clear_cart.process()
        _log('clearcart_%s' % (email), '')
        time.sleep(4 + random.randint(1, 4))

        # multiple gift_cards
        gift_card_list = params['gift_card_list']
        for gift_card in gift_card_list:
            if not gift_card or not gift_card.strip():
                continue
            params['gift_card']['gift_card'] = gift_card
            redeem_gc = RedeemGiftCard(driver, params, account)
            if redeem_gc.navigate():
                redeem_gc.process()
            params['balance'] = redeem_gc.balance

        # multiple asin/keywords
        asin_list = params['asin_list']
        kw_list = params['kw_list']
        brand_list = params['brand_list']
        for i in xrange(len(asin_list)):
            params['asin'] = asin_list[i]
            params['keywords'] = kw_list[i]
            params['brand'] = brand_list[i]

            # search and add to cart
            search = SearchAndGotoAsin(driver, params)
            search.process()
            _log('search_%s' % (keywords.replace(' ', '_')), '')

            add2cart = AddToCart(driver, params, True)
            add2cart.process()
            _log('add2cart_%s_%s' % (keywords.replace(' ', '_'), asin), '')

        checkout_cart = CheckoutCart(driver, params, account)
        checkout_cart.navigate()
        checkout_cart.process()
        _log('checkout_cart_%s_%s' % (keywords.replace(' ', '_'), asin), email)
        time.sleep(4 + random.randint(1, 4))

        # login once again if login page is shown
        signin = SigninWithCaptcha(driver, params, account)
        if signin.is_in_signin_page():
            signin.process()
            _log('resignin_%s_%s' % (keywords.replace(' ', '_'), asin), email)
            time.sleep(4 + random.randint(1, 4))

        # place the order
        place_order = PlaceOrder(driver, params, account)
        place_order.process()
        _log('place_order_%s_%s' % (keywords.replace(' ', '_'), asin), email)

        exit_node = ExitNode(driver, params)
        if exit_node.navigate():
            exit_node.process()

    return _common_process(driver, account, params, _prepare, _process)


def amz_check_account(driver, account, params):
    _log = _gen_log(driver, account, params)

    def _process(driver, account, params):
        # entry_node = EntryNode(driver, params)
        # if entry_node.navigate():
        #     entry_node.process()

        check_prime = PrimeStep(driver, params, account)
        if check_prime.navigate():
            check_prime.process()

        check_gc = CheckGiftCard(driver, params, account)
        if check_gc.navigate():
            check_gc.process()

        log.info('check_account: %s, %s, %s' % (account.get('email'),
                                                check_prime.is_prime,
                                                check_gc.balance))

        # exit_node = ExitNode(driver, params)
        # if exit_node.navigate():
        #     exit_node.process()

    try:
        # home
        home = Home(driver, params)
        home.navigate()
        if not home.is_done():
            _log('Account %s, meet bad proxy ' % account.get('email'), '')
            return

        _log('home', account.get('email'))

        # signin
        signin = SigninWithCaptcha(driver, params, account)
        if not signin.navigate():
            _log('Account %s, meet bad proxy ' % account.get('email'), '')
            return

        signin.process()
        _log('signin', '')
        if signin.is_auth_err():
            _log('Account %s fails the check' % account.get('email'), '')
            return

        _process(driver, account, params)
        _log('Account %s passed the check' % account.get('email'), '')

        return True
    except MeetSpammedAccount as e:
        _log('Account %s fails the check' % account.get('email'), '%s' % e)
    except (StepFailed, CaptchaException) as e:
        # from ipdb import set_trace
        # set_trace()
        # @TODO need to log error message to DB (AmzSaleFarmPrjTask)
        _log('Account %s fails the check' % account.get('email'), '%s' % e)
    except Exception as e:
        # from ipdb import set_trace
        # set_trace()
        _log('Account %s fails the check' % account.get('email'), '%s' % e)
