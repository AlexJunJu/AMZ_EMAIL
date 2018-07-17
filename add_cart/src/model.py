# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import pytz
import logging as log
from random import choice
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
# from sqlalchemy import (create_engine, Column, ForeignKey)
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.engine import reflection
# from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.dialects.postgresql import (TIMESTAMP, BIGINT, VARCHAR, REAL,
                                            BOOLEAN, JSONB, TEXT)
from utils import make_date_period, format_telephone
from config import Configuration

reload(sys)
sys.setdefaultencoding('utf8')

Base = declarative_base()

conf = Configuration.get_instance().data
db_conf = dict(conf['Databases'][0].items()) \
    if conf['System'] == 'test_system' \
    else dict(conf['Databases'][1].items())

port = db_conf.get("port") if db_conf.get("port") is not None else 5432
host = db_conf.get("host")
user = db_conf.get("user")
db_name = db_conf.get("dbname")
pw = db_conf.get("password")
kw_conf = dict(conf['keywords'].items())
RTN_CNT = kw_conf.get("return_count")
title_conf = dict(conf['asin_title'].items())
TITLE_LIMIT = title_conf.get('title_limit')
DEFAULT_GROUP_DESC = "('APS', 'ALL')"
#
#
# engine = create_engine('postgresql://%s:%s@%s/%s?sslmode=require' % (
#     user, pw, host, db_name), max_overflow=20, echo=False,
#     client_encoding='utf8')
#
# DBsession = scoped_session(sessionmaker(bind=engine))
engine = None
DBsession = None


# def inspect():
#     return reflection.Inspector.from_engine(engine)


def fetchall(sql):
    result_proxy = DBsession.execute(sql)
    try:
        return result_proxy.fetchall()
    finally:
        result_proxy.close()


class BaseMethod():

    @classmethod
    def get_all(cls):
        return DBsession.query(cls).all()

    @classmethod
    def get_by_id(cls, id):
        return DBsession.query(cls).filter(cls.id == id).scalar()

    def add(self, commit=True):
        DBsession.add(self)
        if commit:
            return self.commit()
        return True

    def update(self, commit=True):
        DBsession.merge(self)
        if commit:
            return self.commit()
        return True

    @staticmethod
    def execute(sql):
        return DBsession.execute(sql)

    @staticmethod
    def commit():
        try:
            DBsession.commit()
            return True
        except IntegrityError:
            DBsession.rollback()
        except Exception as err:
            DBsession.rollback()
            log.exception(err)
        return False

    # delete True or False:TODO we need to know delete is or not success
    def delete(self, commit=True):
        DBsession.delete(self)
        if commit:
            return self.commit()
        return True


class AmzMarketplace(Base, BaseMethod):
    __tablename__ = 'amz_marketplaces'

    ALL_MARKETS = [
         {'id': 1, 'market_place': 'us', 'website': 'www.amazon.com'},
         {'id': 3, 'market_place': 'uk', 'website': 'www.amazon.co.uk'},
         {'id': 4, 'market_place': 'de', 'website': 'www.amazon.de'},
         {'id': 5, 'market_place': 'fr', 'website': 'www.amazon.fr'},
         {'id': 6, 'market_place': 'jp', 'website': 'www.amazon.co.jp'},
         {'id': 7, 'market_place': 'ca', 'website': 'www.amazon.ca'},
         {'id': 44551, 'market_place': 'es', 'website': 'www.amazon.es'},
         {'id': 35691, 'market_place': 'it', 'website': 'www.amazon.it'},
         ]
    id = Column(BIGINT, primary_key=True)
    market_place = Column(VARCHAR(255))
    website = Column(VARCHAR(255))

    def __repr__(self):
        return '<%s: id=%s, market_place=%s>' % (self.__class__.__name__,
                                                 self.id, self.market_place)

    @classmethod
    def get(cls, id):
        for data in cls.ALL_MARKETS:
            if id != data.get('id'):
                continue
            return AmzMarketplace(
                id=data.get('id'), market_place=data.get('market_place'),
                website=data.get('website'))
        else:
            return None

    @classmethod
    def get_by_market_place(cls, market_place):
        return DBsession.query(cls).filter(cls.market_place == market_place).\
            scalar()

    @classmethod
    def get_by_website(cls, website):
        return DBsession.query(cls).filter(cls.website == website).first()

    @classmethod
    def get_others_marketplace(cls, market):
        ignore_markets = [6]
        ignore_markets.append(market)
        return DBsession.query(cls).filter(~cls.id.in_(ignore_markets)).all()

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return

        for data in cls.ALL_MARKETS:
            market_place = AmzMarketplace(
                id=data.get('id'), market_place=data.get('market_place'),
                website=data.get('website'))
            DBsession.add(market_place)

        try:
            DBsession.commit()
        except Exception:
            DBsession.rollback()

    def to_json(self):
        return {'id': self.id,
                'market_place': self.market_place,
                'website': self.website
                }

    @classmethod
    def is_japan(cls, id):
        return id == 6


class AmzMWSAccount(Base, BaseMethod):
    __tablename__ = 'amz_mws_accounts'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, default=1)
    name = Column(VARCHAR(32), nullable=False)
    merchant_id = Column(VARCHAR(16), nullable=False)
    key = Column(VARCHAR(32), nullable=False)
    secret = Column(VARCHAR(64), nullable=False)

    ALL_ACCOUNTS = [
        {'id': 1, 'marketplace_id': 4, 'name': 'KingLove',
         'merchant_id': 'A2FQRB3OKQXG87',
         'key': 'AKIAI455C5UONC4FBREA',
         'secret': '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'},
        {'id': 2, 'marketplace_id': 1, 'name': 'Yerongzhen',
         'merchant_id': 'ADRAG77Y5JHQM',
         'key': 'AKIAJAN5GVRH6AX2MFEA',
         'secret': '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'},
        {'id': 3, 'marketplace_id': 1, 'name': 'KingLove',
         'merchant_id': 'APH09EB54VUX5',
         'key': 'AKIAIL2OQKM2TOWS6JLA',
         'secret': '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'},
    ]

    @classmethod
    def get_by_market_name(cls, marketplace_id, name):
        for acct in cls.ALL_ACCOUNTS:
            if acct['marketplace_id'] != marketplace_id\
                    or acct['name'] != name:
                continue

            acct = AmzMWSAccount(id=acct['id'],
                                 marketplace_id=acct['marketplace_id'],
                                 name=acct['name'],
                                 merchant_id=acct['merchant_id'],
                                 key=acct['key'],
                                 secret=acct['secret'])
            return acct
        else:
            return None


class MlaProfile(Base, BaseMethod):
    __tablename__ = 'mla_profiles'

    _BROWSER_CHROME = 'chrome'
    _BROWSER_FIREFOX = 'firefox'
    _BROWSER_OPERA = 'opera'
    _BROWSER_STEALTH_FOX = 'stealth_fox'

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    country = Column(VARCHAR(64), nullable=False)
    name = Column(VARCHAR(64), nullable=False)
    profile_id = Column(VARCHAR(64), nullable=False)
    browser = Column(VARCHAR(64), default=_BROWSER_CHROME)
    proxy_host = Column(VARCHAR(64))
    proxy_port = Column(BIGINT)
    used_at = Column(BIGINT, default=0)
    used_by = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)


class AmzAccountInfo(Base, BaseMethod):
    __tablename__ = 'amz_account_infos'

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    password = Column(VARCHAR(64), nullable=False)
    given_name = Column(VARCHAR(64), nullable=False)
    surname = Column(VARCHAR(64), nullable=False)
    # Use as the dummy address
    addr_state = Column(VARCHAR(16), nullable=False)
    addr_state_full = Column(VARCHAR(128))
    addr_city = Column(VARCHAR(64), nullable=False)
    addr_street = Column(VARCHAR(256), nullable=False)
    zip_code = Column(VARCHAR(16), nullable=False)
    # used to recover the account
    telephone = Column(VARCHAR(32), nullable=False)
    telephones = Column(VARCHAR(128), default='')
    ua = Column(VARCHAR(256), default='')
    balance = Column(BIGINT, default=0)
    last_used = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    is_available = Column(BOOLEAN, default=True)

    @classmethod
    def get_by_id(cls, id):
        return DBsession.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_market_email(cls, market_place_id, email):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.email == email).first()

    @classmethod
    def get_all_by_marketplace(cls, market_place_id,
                               is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.is_available == is_available).all()

    def to_json(self):
        return {'market_place_id': self.market_place_id,
                'email': self.email,
                'password': self.password,
                'given_name': self.given_name,
                'surname': self.surname,
                'address_line1': self.addr_street,
                'address_line2': '',
                'city': self.addr_city,
                'state': self.addr_state,
                'zip_code': self.zip_code,
                'telephone': format_telephone(self.telephone),
                'telephones': self.telephones,
                'ua': self.ua,
                'balance': self.balance,
                'last_used': str(self.last_used),
                'is_available': self.is_available}

    @classmethod
    def query_by_marketplace_limit(cls, market_place_id, limit=50,
                                   is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.is_available == is_available).\
            order_by(cls.last_used).limit(limit).all()

    @classmethod
    def query_by_limit(cls, limit=50, is_available=True):
        return DBsession.query(cls).\
            filter(cls.is_available == is_available).\
            order_by(cls.last_used).limit(limit).all()

    @classmethod
    def query_by_marketplace_days_ago(cls, market_place_id, days=7,
                                      is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.last_used <= datetime.utcnow() - timedelta(days=days),
                   cls.is_available == is_available).\
            all()

    @classmethod
    def query_unbind_account(cls, market_place_id,
                             is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.bind_proxy_id == 0,
                   cls.is_available == is_available).all()

    @classmethod
    def query_binding_account(cls, market_place_id,
                              is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.is_available == is_available,
                   cls.bind_proxy_id > 0).all()

    def use(self, commit=True):
        self.last_used = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.update(commit)

    def soft_delete(self, commit=True):
        self.is_available = False
        self.update(commit)

    @classmethod
    def is_account_available(cls, account_id):
        account = cls.get_by_id(account_id)
        return account and account.is_available


class AmzAccountProfileRel(Base, BaseMethod):
    __tablename__ = 'amz_account_profile_rels'

    id = Column(BIGINT, primary_key=True)
    account_id = Column(VARCHAR(64))  # id in AmzAccountInfo
    market_id = Column(BIGINT)  # for multiple markets
    profile_id = Column(VARCHAR(64))  # profile_id in MlaProfile


class AmzFailAccountLog(Base, BaseMethod):
    __tablename__ = 'amz_fail_account_logs'

    id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, nullable=False)
    market_place_id = Column(BIGINT, nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzSaleFarmPrj(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_prjs'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    asin = Column(VARCHAR(16), nullable=False)
    is_adult = Column(BOOLEAN, nullable=False)
    group_desc = Column(VARCHAR(128), default='aps')
    merchant_name = Column(VARCHAR(256))
    brand = Column(VARCHAR(256))
    keywords = Column(VARCHAR(256), nullable=False)
    actual_price = Column(REAL, default=0.0)  # min value is $0.01
    start_date = Column(BIGINT, default=make_date_period)
    end_date = Column(BIGINT)
    plan = Column(JSONB)  # e.g. {date_period: order_cnt}
    has_coupon = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    def to_json(self):
        return {
            'marketplace_id': self.marketplace_id,
            'asin': self.asin,
            'is_adult': self.is_adult,
            'group_desc': self.group_desc,
            'merchant_name': self.merchant_name,
            'brand': self.brand_name,
            'keywords': self.keywords,
            'actual_price': self.actual_price,
        }


class AmzSaleFarmRealAddress(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_real_addresses'

    id = Column(BIGINT, primary_key=True)
    given_name = Column(VARCHAR(64), nullable=False)
    surname = Column(VARCHAR(64), nullable=False)
    telephone = Column(VARCHAR(32), nullable=False)
    country = Column(VARCHAR(64), nullable=False)
    state = Column(VARCHAR(16), default='')
    state_full = Column(VARCHAR(128), default='')
    city = Column(VARCHAR(64), nullable=False)
    address_line1 = Column(VARCHAR(256), nullable=False)
    address_line2 = Column(VARCHAR(256), default='')
    zip_code = Column(VARCHAR(16), nullable=False)
    gate_code = Column(VARCHAR(16), default='')

    @classmethod
    def get_any_by_country(cls, market_id):
        market = AmzMarketplace.get(market_id)
        return choice(DBsession.query(cls).filter(
            cls.country == market.market_place).all())

    def to_json(self):
        from iso_country_codes import get_country_code
        return {
            'given_name': self.given_name,
            'surname': self.surname,
            'country': self.country,
            'country_code': get_country_code(self.country),
            'city': self.city,
            'state': self.state,
            'state_full': self.state_full,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'zip_code': self.zip_code,
            'gate_code': self.gate_code,
            'telephone': self.telephone,
            }


class AmzGiftCard(Base, BaseMethod):
    __tablename__ = 'amz_gift_cards'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    gift_card = Column(VARCHAR(64), default='')
    value = Column(REAL, default=0.0)  # min value is $0.01
    provider = Column(VARCHAR(64), default='')
    is_used = Column(BOOLEAN, default=False)
    used_by = Column(BIGINT, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)


class AmzDebitCard(Base, BaseMethod):
    __tablename__ = 'amz_debit_cards'

    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    CNY = 'CNY'
    JPY = 'JPY'
    AUD = 'AUD'

    id = Column(BIGINT, primary_key=True)
    email = Column(VARCHAR(64), default='')
    source = Column(VARCHAR(64), default='')
    password = Column(VARCHAR(64), default='')
    card_holder = Column(VARCHAR(64), nullable=False)
    card_number = Column(VARCHAR(64), nullable=False)
    expired_date = Column(VARCHAR(64), default='2020-07-31')
    telephone = Column(VARCHAR(64), default='2020-07-31')
    addr_id = Column(BIGINT, default=0)
    balance = Column(BIGINT, default=0)  # min value is $0.01
    currency = Column(BIGINT, default=USD)  # USD/GBP/EUR/CNY/AUD/JPY
    is_used = Column(BOOLEAN, default=False)
    used_by = Column(BIGINT, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'source': self.source,
            'password': self.password,
            'card_holder': self.card_holder,
            'card_number': self.card_number,
            'expired_date': self.expired_date,
            'telephone': self.telephone,
            'addr_id': self.addr_id,
            'balance': self.balance,
            'currency': self.currency if self.currency else self.USD,
        }


class AmzSaleFarmPrjTask(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_prj_tasks'

    _STATE_INIT = 0
    _STATE_SCHEDULED = 1
    _STATE_ADD_TO_CART = 2
    _STATE_ADD_TO_WISH = 3
    _STATE_ORDER_DONE = 4
    _STATE_SHIPMENT_DONE = 5
    _STATE_REVIEW_DONE = 6

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT, ForeignKey('amz_sale_farm_prjs.id'))
    state = Column(BIGINT, default=_STATE_INIT)
    addr_id = Column(BIGINT, default=0)
    buyer_id = Column(BIGINT, default=0)
    debit_card_id = Column(BIGINT, default=0)
    order_no = Column(VARCHAR(64), default='')
    shipment_no = Column(VARCHAR(64), default='')
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)
    scheduled_at = Column(TIMESTAMP(timezone=True))
    carted_at = Column(TIMESTAMP(timezone=True))
    wished_at = Column(TIMESTAMP(timezone=True))
    ordered_at = Column(TIMESTAMP(timezone=True))
    shipped_at = Column(TIMESTAMP(timezone=True))
    reviewed_at = Column(TIMESTAMP(timezone=True))
    comments = Column(TEXT, default='')


if __name__ == '__main__':
    from ipdb import set_trace
    set_trace()
