# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import json
import time
import pytz
import re
import logging as log
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import (create_engine, orm, Column, Integer, Boolean, true,Date,Numeric,
                        select, ForeignKey, func, or_, not_,and_,literal,desc,asc)
from sqlalchemy.sql.schema import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import reflection
from sqlalchemy.orm import (Session, scoped_session, sessionmaker,
                            object_session)
from sqlalchemy.databases import postgresql
from sqlalchemy.dialects.postgresql import (ARRAY, TIMESTAMP, BIGINT, VARCHAR,
                                            REAL, BOOLEAN, JSONB, BIT, TEXT,
                                            TSVECTOR)
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import ClauseList

# from redis_utils import RedisUtils
from random import choice
from collections import OrderedDict
from config import Configuration
from utils import (Singleton, Sync, format_group, format_to_group_map,
                   format_translation, category_format_to_arg, Proxyip,
                   make_last_month_period, make_last_year_month_period,
                   Probability,
                   make_month_before_last_month_period)

from imp import reload
reload(sys)
#python3 取消了setdefaultencoding
#sys.setdefaultencoding('utf8') 

Base = declarative_base()

conf = Configuration.get_instance().data

#conf,是一个python的dict类型
#dict(),用于创建一个字典，返回一个字典
#字典 items(),以列表返回可遍历的(键, 值) 元组数组
#conf['Databases'][0].items()，访问字典里key为'Databases'的value——list中的第0个元素——item()返回的可遍历的由元组组成的数组列表


#反斜杠作为续行符，貌似只有else起作用
db_conf = dict(conf['Databases'][0].items()) \
    if conf['System'] == 'test_system' \
    else dict(conf['Databases'][1].items())

#获取数据库预连接信息
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


#创建数据库连接引擎
# engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s?sslmode=require' % (
#     user, pw, host, db_name), max_overflow=20, echo=False,
#     client_encoding='utf8')

# engine_autocommit = create_engine('postgresql+psycopg2://%s:%s@%s/%s?sslmode=require' %
#                                   (user, pw, host, db_name),
#                                   pool_size=2, max_overflow=0,
#                                   echo=True,
#                                   client_encoding='utf8',
#                                   isolation_level='AUTOCOMMIT')




engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s?sslmode=require' % (
    user, pw, '127.0.0.1:5432', db_name), max_overflow=20, echo=False,
    client_encoding='utf8')


# engine_autocommit = create_engine('postgresql+psycopg2://%s:%s@%s/%s?sslmode=require' %
#                                   (user, pw, '127.0.0.1:5432', db_name),
#                                   pool_size=2, max_overflow=0,
#                                   echo=True,
#                                   client_encoding='utf8',
#                                   isolation_level='AUTOCOMMIT')
#                                   
# engine  = create_engine('postgresql+psycopg2://ecsp_dev:maxsonic@127.0.0.1:5432/ecsp_dev_db',max_overflow=20, echo=False,client_encoding='utf8')#不能用主机名，需用IP地址

# engine_autocommit = create_engine('postgresql+psycopg2://ecsp_dev:maxsonic@127.0.0.1:5432/ecsp_dev_db',
#                                   pool_size=2, max_overflow=0,
#                                   echo=True,
#                                   client_encoding='utf8',
#                                   isolation_level='AUTOCOMMIT')



def inspect():
    return reflection.Inspector.from_engine(engine)


def fetchall(sql):
    #execute() 返回值的结果？？？？
    result_proxy = DBsession.execute(sql)

    print(type(result_proxy))
    try:
        return result_proxy.fetchall()
    finally:
        result_proxy.close()


def create_sql_code(proxy_table, speed_table, target, type, country, level,
                    min_score, num):
    a = '''
    SELECT
        {proxy_table}.id
    FROM {proxy_table} INNER JOIN {speed_table}
    ON {proxy_table}.id = {speed_table}.proxy_id
    WHERE useful = 't' AND score >= {min_score} {sql} ORDER BY last_used
    LIMIT {num}
    '''
    sql = ''
    if target:
        sql += "AND target = %s " % target.id
    if type:
        sql += "AND %s.type = '%s' " % (proxy_table, type.lower())
    if country:
        sql += "AND country = '%s' " % country
    if level:
        sql += 'AND level = %s ' % str(level)

    return a.format(**{'proxy_table': proxy_table, 'speed_table': speed_table,
                    'min_score': min_score, 'sql': sql, 'num': num})


def rank_keywords(marketplace_id, group, cate, limit=RTN_CNT):
    lang_map = {1: 'english', 3: 'english', 7: 'english', 4: 'german',
                5: 'french', 35691: 'italian', 44551: 'spanish'}
    language = 'english'
    cate_list = []
    cate = cate.strip()
    c = format_to_group_map(cate)
    if lang_map.get(marketplace_id) != 'english':
        translation_sql = '''
                        SELECT * FROM amz_translation_datas WhERE text='%s'
                        And marketplace_id=%s
                        ''' % (c, marketplace_id)
        translation_result = fetchall(translation_sql)
        if translation_result:
            for t_result in translation_result:
                format_result = format_translation(t_result[3])
                cate_list.extend(format_result)
    else:
        cate_list = category_format_to_arg([cate])
    final_cate = ' | '.join(cate_list)
    rank_sql = '''
    SELECT category_orgin, subcategory_orgin
    FROM (SELECT amz_list_datas.category as category,
        amz_list_datas.subcategory as subcategory,
        amz_list_datas.subcategory_orgin as subcategory_orgin,
        amz_list_datas.category_orgin as category_orgin,
        amz_list_datas.marketplace_id as marketplace_id,
        amz_list_datas.group_name as group_name,
        setweight(to_tsvector(amz_list_datas.category), 'B') ||
        setweight(to_tsvector(amz_list_datas.subcategory), 'A') as document
        FROM amz_list_datas) p_search
    WHERE p_search.document @@ to_tsquery('%s', $maxsonic$%s$maxsonic$)
    and marketplace_id=%s
    and group_name in %s
    ORDER BY ts_rank(p_search.document, to_tsquery('%s',
    $maxsonic$%s$maxsonic$)) DESC LIMIT %d;
    '''
    final_rank_sql = rank_sql % (language, final_cate, marketplace_id,
                                 format_group(group), language, final_cate,
                                 limit)
    change_conf = "SET default_text_search_config = 'pg_catalog.english';"
    DBsession.execute(change_conf)
    rank_result = fetchall(final_rank_sql)
    cate_sql = '''
    SELECT keywords, sum(search_count) as cnt FROM amz_all_category_datas WHERE
    marketplace_id=%s AND product_group IN %s AND format_cate || '--' ||
    format_subcate in (%s) GROUP BY keywords ORDER BY cnt
    DESC LIMIT %d;'''

    if rank_result:
        cate_subcate = []
        for result in rank_result:
            new_key = "'%s--%s'" % (result[0], result[1])
            cate_subcate.append(new_key)
        find_cate_sql = cate_sql % (marketplace_id, group,
                                    ','.join(cate_subcate), limit)
        cate_result = fetchall(find_cate_sql)
        return_keywords = []
        for r in cate_result:
            return_keywords.append(r[0])
        return return_keywords
    else:
        return None


class _Session(Session):

    def __init__(self, **kw):
        Session.__init__(self, **kw)
        self._updates = set()
        self._deletes = set()

DBsession = scoped_session(sessionmaker(bind=engine, class_=_Session))

# DBsession_autocommit = scoped_session(sessionmaker(bind=engine_autocommit))



#创建基类模块方法，为数据库各表提供基本的公用操作
class BaseMethod():

    #使用@staticmethod跟@classmethod，可以不需要实例化，可以直接类名.(属性)方法名()调用
    #@staticmethod不需要表示自身对象的self和自身类的cls参数，跟使用函数一样
    #@classmethod需要self参数，但第一个参数必须是表示自身类cls参数
    #如果在@staticmethod中要调用到这个类的属性、方法，只能直接类名.属性名、类名.方法名
    #@classmethod因为持有cls参数，可以直接调用类的属性、方法、实例化对象，避免硬编码


    #查询所有制定表的信息
    @classmethod
    def get_all(cls):
        return DBsession.query(cls).all()

    #根据id标量（Scalar）查询相关表的信息
    @classmethod
    def get_by_id(cls, id):
        return DBsession.query(cls).filter(cls.id == id).scalar()


    #根据提交状态来进行插入操作，这样做的目的是一次性写入，减少数据库操作开销
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


    #注意commit()方法跟commit变量的区别
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

#基类代理服务器方法
class BaseProxy(BaseMethod):
    id = Column(BIGINT, primary_key=True)
    ip = Column(VARCHAR(32), nullable=False)
    port = Column(BIGINT, nullable=False)
    type = Column(VARCHAR(16), nullable=False)
    level = Column(BIGINT)
    isp = Column(VARCHAR(256), nullable=True)
    country = Column(VARCHAR(64))
    region = Column(VARCHAR(64))
    city = Column(VARCHAR(64))
    useful = Column(BOOLEAN, default=False)
    last_used = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    create_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    TABLE_NAME = ''
    SPEED_TABLE_NAME = ''
    MIN_SCORE = 80

    def update(self, commit=True):
        self.last_used = datetime.utcnow().replace(tzinfo=pytz.UTC)
        DBsession.merge(self)
        if commit:
            self.commit()

    @classmethod
    def get_country_by_market(cls, market):
        market_country_map = {1: "US", 3: "EU", 4: "EU", 5: "EU", 6: "JP",
                              7: "US", 35691: "EU", 44551: "EU"}

        return market_country_map.get(market, 'US')

    @classmethod
    def get_by_id(cls, id):
        '''
        https://github.com/NewTrident/ECSP-Service/issues/78
        '''
        return DBsession.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_one(cls):
        return choice(cls.get_all())

    @staticmethod
    def get_proxy(cls, type=None, target=None, level=None, country=None):
        def _get_proxy_list(target, type, level, country):
            min_score = cls.MIN_SCORE
            proxy_id_list = fetchall(create_sql_code(cls.TABLE_NAME,
                                                     cls.SPEED_TABLE_NAME,
                                                     target, type, country,
                                                     level, min_score, 1))
            return [p['id'] for p in proxy_id_list]

        if target:
            target = ECSPTarget.get_by_target(target.lower())

        if country and country != 'US' and Probability.less_than(30):
            country = 'US'

        proxy_ids = _get_proxy_list(target, type, level, country)
        if not proxy_ids and country != 'US':
            proxy_ids = _get_proxy_list(target, type, level, 'US')
        if not proxy_ids:
            return None

        DBsession.query(cls).filter(cls.id.in_(proxy_ids)).\
            update({cls.last_used: datetime.now().replace(tzinfo=pytz.UTC)},
                   synchronize_session=False)
        DBsession.commit()
        proxy_list = DBsession.query(cls).filter(cls.id.in_(proxy_ids)).all()
        if not proxy_list:
            return None

        if not hasattr(proxy_list[0], 'username'):
            return Proxyip(ip=proxy_list[0].ip, port=proxy_list[0].port,
                           type=proxy_list[0].type)

        return Proxyip(ip=proxy_list[0].ip,
                       port=proxy_list[0].port,
                       type=proxy_list[0].type,
                       username=proxy_list[0].username,
                       password=proxy_list[0].password)

    def to_json(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'type': self.type,
            'level': self.level,
            }


class BaseProxySpeed(BaseMethod):
    id = Column(BIGINT, primary_key=True)
    proxy_id = Column(BIGINT, nullable=False)
    ip = Column(VARCHAR(32), nullable=False)
    port = Column(BIGINT, nullable=False)
    type = Column(VARCHAR(16), nullable=False)
    target = Column(BIGINT, nullable=False)
    score = Column(BIGINT, nullable=False)
    update_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    def update(self, commit=True):
        self.update_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        DBsession.merge(self)
        if commit:
            self.commit()

    @classmethod
    def get_all_by_target(cls, target):
        return DBsession.query(cls).filter(cls.target == target).all()

    @classmethod
    def query_by_ip_and_target(cls, ip, port, target):
        return DBsession.query(cls).filter(cls.ip == ip, cls.port == port,
                                           cls.target == target).first()

    @classmethod
    def get_by_target_score(cls, target, score=0):
        return DBsession.query(cls).filter(cls.target == target,
                                           cls.score >= score).all()

    @classmethod
    def delete_unuseful(cls):
        DBsession.query(cls).filter(cls.score < 0).delete()
        DBsession.commit()

    @staticmethod
    def get_score(timeused):
        return int(100 - timeused)

    def increase_score(self, value, commit=True):
        expect_second = 16
        if value > expect_second:
            self.decrease_score(10, commit)
        else:
            if not self.score:
                self.score = 80
            else:
                self.score = self.score + (150/self.score) *\
                    (expect_second - int(value))
            self.update(commit)

    def decrease_score(self, value, commit=True):
        self.score = 70 if self.score >= 80 else self.score - value
        self.update(commit)


class User(Base):
    __tablename__ = 'users'
    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False)
    salt = Column(VARCHAR(255))
    group_id = Column(BIGINT, nullable=False)
    manager_id = Column(BIGINT)
    profile = Column(VARCHAR(65535))
    status = Column(BOOLEAN)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))
    deleted_at = Column(TIMESTAMP(timezone=True))
    notif_ids = Column(ARRAY(Integer))
    unread_ids = Column(ARRAY(Integer))

    @classmethod
    def get_all(cls):
        return DBsession.query(cls).all()

    @classmethod
    def get(cls, id):
        return DBsession.query(cls).filter(cls.id == id,).scalar()

    @classmethod
    def _get_subdict(cls, parent, child_name):
        return parent[child_name]\
            if type(parent) is dict and child_name in parent else {}

    def get_profile(self):
        # XXX: To avoid a bug that the profile is a json with //" rather than
        # /"
        profile = json.loads(self.profile) if self.profile else {}

        return profile if type(profile) is dict else json.loads(profile)

    def is_admin(self):
        return self.group_id == 2 or self.group_id == 1

    @classmethod
    def get_by_email_group(cls, email, group):
        return DBsession.query(cls).filter(cls.email == email,
                                           cls.group_id == group).first()


class ECSPProxyips(Base, BaseProxy):
    __tablename__ = 'ecsp_proxyips'
    update_at = Column(BIGINT, default=0)
    __table_args__ = (Index('proxyips_idx', 'ip', 'port', unique=True),)

    TABLE_NAME = 'ecsp_proxyips'
    SPEED_TABLE_NAME = 'ecsp_proxy_speeds'

    def add(self, commit=True):
        # To prevent from tons of the db error
        # duplicate key value violates unique constraint "proxyips_idx"
        try_one = DBsession.query(ECSPProxyips)\
            .filter(ECSPProxyips.ip == self.ip,
                    ECSPProxyips.port == self.port)\
            .first()
        if try_one:
            return False

        DBsession.add(self)
        if commit:
            return self.commit()
        return True

    @classmethod
    def get_proxy(cls, type=None, target=None, level=None, country=None):
        return BaseProxy.get_proxy(cls, type, target, level, None)

    @classmethod
    def delete_unuseful(cls):
        nowtime = time.time()
        DBsession.query(cls).filter((nowtime - cls.update_at) > 86400).delete()
        DBsession.commit()

    @classmethod
    def get_all_can_use(cls):
        return DBsession.query(cls).filter(cls.useful == true()).all()


class ECSPProxySpeed(Base, BaseProxySpeed):
    __tablename__ = 'ecsp_proxy_speeds'
    __table_args__ = (Index('proxyspeeds_idx', 'proxy_id', 'target',
                            unique=True),)
    __SCORE = 70

    @classmethod
    def get_by_target_score(cls, target, score=70):
        return DBsession.query(cls).filter(cls.target == target,
                                           cls.score >= score).all()

    @classmethod
    def delete_unuseful(cls):
        DBsession.query(cls).filter(cls.score < 70).delete()
        DBsession.commit()


class ECSPTarget(Base, BaseMethod):
    __tablename__ = 'ecsp_targets'
    id = Column(BIGINT, primary_key=True)
    target = Column(VARCHAR(32), nullable=False, unique=True)
    url = Column(JSONB, nullable=False, unique=True)
    type = Column(VARCHAR(16), nullable=False)
    test_str = Column(VARCHAR(256), nullable=False)
    size = Column(BIGINT)

    @classmethod
    def get_by_target(cls, target):
        return DBsession.query(cls).filter(cls.target == target).first()

    def get_url_by_market(self, market):
        return self.url.get(market, 'https://www.amazon.com')


class ECSPUserAgent(Base, BaseMethod):
    __tablename__ = 'ecsp_user_agents'
    id = Column(BIGINT, primary_key=True)
    user_agent = Column(VARCHAR(256), nullable=False)
    brower = Column(VARCHAR(64))
    system = Column(VARCHAR(64))
    __table_args__ = (Index('user-agents_idx', 'user_agent', unique=True),)
    __user_agent_cache = []

    _DEFAULT_UA = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 ' +\
        '(KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'

    @classmethod
    def get_all(cls):
        if cls.__user_agent_cache != []:
            return cls.__user_agent_cache
        return DBsession.query(cls).all()

    @classmethod
    def _default_ua(cls):
        return cls(user_agent=cls._DEFAULT_UA)

    @classmethod
    def get_one(cls):
        all_uas = cls.get_all()
        return choice(all_uas) if all_uas else cls._default_ua()

    @classmethod
    def get_by_brower(cls, bor):
        return choice([u for u in cls.get_all() if u.brower.startswith(bor)])

    @classmethod
    def get_by_system(cls, sys):
        return choice([u for u in cls.get_all() if u.system.startswith(sys)])


class ECSPPrivateProxy(Base, BaseProxy):
    __tablename__ = 'ecsp_private_proxys'
    NORMAL_PROXY = 1
    IMPR_PROXY = 2
    IMPR_CPC_PROXY = 3
    FARM_PROXY = 4
    SUN_PROXY = 5

    username = Column(VARCHAR(32))
    password = Column(VARCHAR(32))
    havespeed = Column(BOOLEAN, default=False)
    expiry_date = Column(TIMESTAMP(timezone=True))
    is_rotating = Column(BOOLEAN, default=False)
    proxy_type = Column(BIGINT, default=NORMAL_PROXY)
    bind_account_count = Column(BIGINT, default=0)
    __table_args__ = (Index('private_proxys_idx', 'ip', 'port', unique=True),)

    TABLE_NAME = 'ecsp_private_proxys'
    SPEED_TABLE_NAME = 'ecsp_private_proxy_speeds'

    @staticmethod
    def _query_proxy(target, typ='https', level=1, country='US', min_score=10,
                     num=1, func_type_filter=None):
        def _do_query(target_id, typ, level, country):
            query_ = DBsession.query(ECSPPrivateProxy).\
                join(ECSPPrivateProxySpeed,
                     ECSPPrivateProxy.id == ECSPPrivateProxySpeed.proxy_id).\
                filter(ECSPPrivateProxy.useful == true(),
                       ECSPPrivateProxy.country == country,
                       ECSPPrivateProxySpeed.type == typ,
                       ECSPPrivateProxySpeed.target == target_id,
                       ECSPPrivateProxySpeed.score >= min_score)
            if func_type_filter:
                query_ = func_type_filter(query_)

            return query_.order_by(ECSPPrivateProxy.last_used).limit(num).all()

        if target:
            target = ECSPTarget.get_by_target(target.lower())
        if country and country != 'US' and Probability.less_than(30):
            country = 'US'

        proxies = _do_query(target.id, typ, level, country)
        if not proxies and country != 'US':
            proxies = _do_query(target.id, typ, level, 'US')
        if not proxies:
            return None

        proxy = proxies[0]
        proxy_ip = Proxyip(ip=proxy.ip, port=proxy.port, type=proxy.type,
                           username=proxy.username, password=proxy.password)
        proxy.update()
        return proxy_ip

    @classmethod
    def get_proxy(cls, typ='https', target='amazon', level=1, country='US'):
        def _filter(query_):
            if not query_:
                return None
            func_types = [cls.NORMAL_PROXY, cls.IMPR_PROXY]
            return query_.filter(cls.proxy_type.in_(func_types))

        return ECSPPrivateProxy._query_proxy(target, typ=typ, level=level,
                                             country=country,
                                             func_type_filter=_filter)

    @classmethod
    def get_impr_proxy(cls, typ='https', target='amazon', country='US'):
        def _filter(query_):
            if not query_:
                return None
            func_types = [cls.IMPR_PROXY, cls.IMPR_CPC_PROXY]
            return query_.filter(cls.proxy_type.in_(func_types))

        return ECSPPrivateProxy._query_proxy(target, typ=typ, level=1,
                                             country=country,
                                             func_type_filter=_filter)

    @classmethod
    def get_cpc_proxy(cls, typ='https', target='amazon', country='US'):
        def _filter(query_):
            if not query_:
                return None
            func_types = [cls.IMPR_CPC_PROXY]
            return query_.filter(cls.proxy_type.in_(func_types))

        return ECSPPrivateProxy._query_proxy(target, typ=typ, level=1,
                                             country=country,
                                             func_type_filter=_filter)

    @classmethod
    def get_sun_proxy(cls, typ='https', target='amazon', country='US'):
        def _filter(query_):
            if not query_:
                return None
            func_types = [cls.SUN_PROXY]
            return query_.filter(cls.proxy_type.in_(func_types))

        return ECSPPrivateProxy._query_proxy(target, typ=typ, level=1,
                                             country=country,
                                             func_type_filter=_filter)

    @classmethod
    def get_all_proxies(cls):
        return DBsession.query(cls).all()

    @classmethod
    def get_by_havespeed(cls, havespeed, proxy_type=NORMAL_PROXY):
        return DBsession.query(cls).\
            filter(cls.havespeed == havespeed,
                   cls.proxy_type == proxy_type).all()

    @classmethod
    def get_by_useful(cls, useful, proxy_type=NORMAL_PROXY):
        return DBsession.query(cls).\
            filter(cls.useful == useful,
                   cls.proxy_type == proxy_type).all()

    @classmethod
    def delete_unuseful(cls, proxy_type=NORMAL_PROXY):
        now_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        DBsession.query(cls).\
            filter(cls.expiry_date < now_time,
                   cls.proxy_type == proxy_type).delete()
        DBsession.commit()

    @classmethod
    def query_valid_farm_proxies(cls, bind_account_count=5):
        return DBsession.query(cls).\
            filter(cls.bind_account_count < bind_account_count,
                   cls.proxy_type == cls.FARM_PROXY).all()

    @classmethod
    def get_proxy_by_proxy_id(cls, proxy_id):
        proxy = ECSPPrivateProxy.get_by_id(proxy_id)
        if not proxy:
            return None
        proxy.last_used = datetime.now().replace(tzinfo=pytz.UTC)
        proxy.commit()
        return Proxyip(ip=proxy.ip, port=proxy.port, type=proxy.type,
                       username=proxy.username, password=proxy.password)

    def to_json(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'type': self.type,
            'level': self.level,
            'username': self.username,
            'password': self.password
            }


class ECSPPrivateProxySpeed(Base, BaseProxySpeed):
    __tablename__ = 'ecsp_private_proxy_speeds'
    '''
        rotating proxy will auto change proxy IP periodically
        so the proxy speed is meaningless
    '''
    is_rotating = Column(BOOLEAN, default=False)
    __table_args__ = (Index('private_proxy_speeds_idx', 'proxy_id', 'target',
                            unique=True),)

    @classmethod
    def get_by_target_score(cls, target, score=0):
        return DBsession.query(cls).filter(cls.target == target,
                                           cls.is_rotating != true(),
                                           cls.score >= score).all()

    @classmethod
    def delete_unuseful(cls):
        query_proxy_ids = select([ECSPPrivateProxy.id])
        DBsession.query(cls).filter(cls.proxy_id.notin_(query_proxy_ids)).\
            delete(synchronize_session='fetch')
        DBsession.commit()

    @classmethod
    def reset(cls):
        dt = datetime.utcnow() - timedelta(days=1)
        proxies = DBsession.query(cls).\
            filter(cls.score <= 0, cls.update_at < dt).all()
        for proxy in proxies:
            proxy.score = 100
            proxy.update(commit=False)
        BaseMethod.commit()

    def decrease_score(self, value, commit=True):
        if self.is_rotating:
            return

        BaseProxySpeed.decrease_score(self, value, commit)


class AmzMarketplace(Base, BaseMethod):
    __tablename__ = 'amz_marketplaces'

    id = Column(BIGINT, primary_key=True)
    market_place = Column(VARCHAR(255))
    website = Column(VARCHAR(255))

    def __repr__(self):
        return '<%s: id=%s, market_place=%s>' % (self.__class__.__name__,
                                                 self.id, self.market_place)

    @classmethod
    def get(cls, id):
        return DBsession.query(cls).filter(cls.id == id,).scalar()

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

        all_market_places = [
            {'id': 1, 'market_place': 'us', 'website': 'www.amazon.com'},
            {'id': 3, 'market_place': 'uk', 'website': 'www.amazon.co.uk'},
            {'id': 4, 'market_place': 'de', 'website': 'www.amazon.de'},
            {'id': 5, 'market_place': 'fr', 'website': 'www.amazon.fr'},
            {'id': 6, 'market_place': 'jp', 'website': 'www.amazon.co.jp'},
            {'id': 7, 'market_place': 'ca', 'website': 'www.amazon.ca'},
            {'id': 44551, 'market_place': 'es', 'website': 'www.amazon.es'},
            {'id': 35691, 'market_place': 'it', 'website': 'www.amazon.it'},
            ]

        for data in all_market_places:
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



def make_date_period(dt=None):
    """
    input a datetime instance return an int
    """
    if not dt:
        dt = datetime.utcnow()
    return int(dt.strftime('%Y%m%d'))


def make_month_period(dt=None):
    """
    input a datetime instance return an int
    """
    if not dt:
        dt = datetime.utcnow()
    return int(dt.strftime('%Y%m'))



class AmzKeywordsRanking(Base, BaseMethod):
    __tablename__ = 'amz_keywords_rankings'

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    # by default it is aps, i.e. all products search
    group_desc = Column(VARCHAR(128), default='aps')
    keywords = Column(VARCHAR(512), nullable=False)
    # e.g. 20150118/20160101
    date_period = Column(BIGINT, default=make_date_period)
    ranking1 = Column(JSONB)
    ranking1_at = Column(TIMESTAMP(timezone=True))
    ranking2 = Column(JSONB)
    ranking2_at = Column(TIMESTAMP(timezone=True))
    ranking3 = Column(JSONB)
    ranking3_at = Column(TIMESTAMP(timezone=True))

    __table_args__ = (Index('amz_kw_idx_1', 'market_place_id', 'group_desc',
                            'keywords', unique=False),)

    def query_by_variants(self, asin):
        all_children = AmzAsinVariants.\
            get_same_parent_asins(asin, self.market_place_id)

        if not all_children:
            return None

        child_rank_dict = {}
        for child in all_children:
            rank = self.get_asin_ranking(child)
            if rank:
                child_rank_dict[asin] = rank

        if not child_rank_dict:
            return None

        rank = sorted(child_rank_dict.items(),
                      key=lambda x: x[1])[0][1]
        return rank

    @classmethod
    def query_all_kw_data_per_date(cls, market_place_id, group='aps',
                                   today=make_date_period()):
        return DBAmzOrder.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.group_desc == group,
            cls.date_period == today).all()

    @classmethod
    def query_by_kw_and_today(cls, market_place_id, keywords, group, asin):
        today = make_date_period()
        today_search = DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            func.lower(cls.keywords) == keywords.lower(),
            cls.group_desc == group,
            cls.date_period == today).first()
        if today_search:
            rank = today_search.get_asin_ranking(asin)
            return rank if rank else today_search.query_by_variants(asin)

        return None

    @classmethod
    def query_by_keywords(cls, market_place_id, keywords):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.keywords == keywords).order_by(cls.date_period.desc()).all()

    @classmethod
    def query_by_keywords_period(cls, market_place_id, keywords, start, end,
                                 group_desc='aps'):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.keywords == keywords,
            cls.group_desc == group_desc,
            cls.date_period >= start,
            cls.date_period <= end).order_by(cls.date_period.desc()).all()

    @classmethod
    def query_by_keywords_latest(cls, market_place_id, keywords,
                                 group_desc='aps'):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.group_desc == group_desc,
            cls.keywords == keywords).order_by(cls.date_period.desc()).first()

    @classmethod
    def query_by_kw_list_latest(cls, market_place_id, kw_list, start, end):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.keywords.in_(kw_list),
            cls.date_period >= start,
            cls.date_period <= end).order_by(cls.date_period.desc()).all()

    def update(self, ranking):
        if self.ranking1 is None or len(self.ranking1) == 0:
            self.ranking1 = ranking
            self.ranking1_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        elif self.ranking2 is None or len(self.ranking2) == 0:
            self.ranking2 = ranking
            self.ranking2_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        elif self.ranking3 is None or len(self.ranking3) == 0:
            self.ranking3 = ranking
            self.ranking3_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        else:
            return

        DBsession.merge(self)
        try:
            DBsession.commit()
        except Exception as err:
            DBsession.rollback()
            log.exception(err)

    @classmethod
    def store_keywords_ranking(cls, market_place_id, keywords, group_desc,
                               date_period, result):
        kw_ranking = AmzKeywordsRanking.query_by_keywords_period(
            market_place_id=market_place_id, keywords=keywords,
            group_desc=group_desc, start=date_period, end=date_period)

        if not kw_ranking:
            kw_ranking = AmzKeywordsRanking(market_place_id=market_place_id,
                                            keywords=keywords,
                                            group_desc=group_desc,
                                            ranking1=result,
                                            ranking1_at=datetime.utcnow())
            kw_ranking.add()
        else:
            kw_ranking[0].update(result)

    def get_asin_ranking(self, asin):
        result = {}

        def _get(rankings, ranking_at):
            if rankings is None or asin not in rankings:
                return
            result[ranking_at.strftime('%Y%m%d')] = rankings[asin]
            # XXX: when ECSP chart change better, then back up
            # result[ranking_at.strftime('%Y%m%d %H:%M:%S')] = rankings[asin]

        _get(self.ranking1, self.ranking1_at)
        _get(self.ranking2, self.ranking2_at)
        _get(self.ranking3, self.ranking3_at)

        return result


class AmzMerchantInfo(Base, BaseMethod):
    __tablename__ = 'amz_merchant_infos'

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    merchant_name = Column(VARCHAR(256), nullable=False)
    merchant_id = Column(VARCHAR(64), nullable=False)

    @classmethod
    def get_by_merchant_id(cls, market_place_id, merchant_id):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.merchant_id == merchant_id).first()

    @classmethod
    def save(cls, market_place_id, merchant_name, merchant_id):
        obj = cls.get_by_merchant_id(market_place_id, merchant_id)
        if obj is None:
            obj = AmzMerchantInfo(market_place_id=market_place_id,
                                  merchant_name=merchant_name,
                                  merchant_id=merchant_id)
            obj.add()


class AmzAsinOffer(Base, BaseMethod):
    __tablename__ = 'amz_asin_offers'

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    merchant_id = Column(VARCHAR(64), nullable=False)
    offer_listing_id = Column(VARCHAR(256), nullable=False)
    is_fba = Column(Boolean, default=False)

    _SQL_QUERY_TRACKED_ASIN_OFFERS = '''
    SELECT amz_user_tracked_asins.id AS id,
    amz_asin_offers.market_place_id AS market_place_id,
    amz_asin_offers.asin AS asin
    FROM amz_asin_offers INNER JOIN amz_user_tracked_asins
    ON amz_asin_offers.id=amz_user_tracked_asins.asin_offer_id
    WHERE amz_user_tracked_asins.user_id={user_id}
    '''

    @classmethod
    def get_by_asin_merchant(cls, market_place_id, asin, merchant_id):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.asin == asin,
            cls.merchant_id == merchant_id).first()

    @classmethod
    def query_by_asin(cls, market_place_id, asin):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            cls.asin == asin).all()

    @classmethod
    def query_by_userid(cls, user_id):
        return DBsession.query(cls).join(AmzUserTrackedAsin).\
            filter(AmzUserTrackedAsin.user_id == user_id).all()

    @classmethod
    def query_all_tracked_offers(cls):
        return DBsession.query(cls).join(AmzUserTrackedAsin).all()

    @classmethod
    def query_track_asin_offers_by_userid(cls, user_id):
        sql = cls._SQL_QUERY_TRACKED_ASIN_OFFERS.format(**{'user_id': user_id})
        return fetchall(sql)

    @classmethod
    def save(cls, market_place_id, asin, merchant_id, offer_id, is_fba,
             commit=True):
        if not offer_id or not merchant_id or not asin:
            return None

        obj = cls.get_by_asin_merchant(market_place_id, asin, merchant_id)
        if obj is None:
            obj = AmzAsinOffer(market_place_id=market_place_id,
                               asin=asin,
                               merchant_id=merchant_id,
                               offer_listing_id=offer_id,
                               is_fba=is_fba)
            obj.add(commit=False)
            if commit:
                obj.commit()

        return obj


class AmzUserTrackedAsin(Base, BaseMethod):
    __tablename__ = 'amz_user_tracked_asins'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    asin_offer_id = Column(BIGINT, ForeignKey('amz_asin_offers.id'))

    @classmethod
    def query_by_userid(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def query_by_userid_asin(cls, user_id, market, asin):
        return DBsession.query(cls).join(AmzAsinOffer).\
            filter(cls.user_id == user_id,
                   AmzAsinOffer.market_place_id == market,
                   AmzAsinOffer.asin == asin).first()

    @classmethod
    def save(cls, user_id, asin_offer_id, commit=True):
        obj = DBsession.query(cls).filter(
            cls.user_id == user_id,
            cls.asin_offer_id == asin_offer_id).first()
        if obj is not None:
            return

        obj = AmzUserTrackedAsin(user_id=user_id, asin_offer_id=asin_offer_id)
        obj.add(commit=False)
        if commit:
            obj.commit()


class AmzUserTrackedAsinStock(Base, BaseMethod):
    __tablename__ = 'amz_user_tracked_asin_stocks'

    id = Column(BIGINT, primary_key=True)
    asin_offer_id = Column(BIGINT, ForeignKey('amz_asin_offers.id'))
    # e.g. 20150118/20160101
    date_period = Column(BIGINT, default=make_date_period)
    stock1 = Column(BIGINT, default=0)
    stock1_at = Column(TIMESTAMP(timezone=True))
    stock2 = Column(BIGINT, default=0)
    stock2_at = Column(TIMESTAMP(timezone=True))
    stock3 = Column(BIGINT, default=0)
    stock3_at = Column(TIMESTAMP(timezone=True))

    @classmethod
    def query_by_offer(cls, asin_offer_id):
        return DBsession.query(cls).filter(
            cls.asin_offer_id == asin_offer_id).\
            order_by(cls.date_period.desc()).all()

    @classmethod
    def query_by_offer_period(cls, asin_offer_id, start, end):
        return DBsession.query(cls).filter(
            cls.asin_offer_id == asin_offer_id,
            cls.date_period >= start,
            cls.date_period <= end).order_by(cls.date_period.desc()).all()

    @classmethod
    def store_offer_stock(cls, asin_offer_id, stock, date_period):
        stocks = AmzUserTrackedAsinStock.query_by_offer_period(
            asin_offer_id=asin_offer_id, start=date_period, end=date_period)

        if not stocks:
            stock = AmzUserTrackedAsinStock(asin_offer_id=asin_offer_id,
                                            stock1=stock,
                                            stock1_at=datetime.utcnow())
            stock.add()
        else:
            stocks[0].update(stock)

    def update(self, stock):
        if self.stock1 is None or self.stock1 == 0:
            self.stock1 = stock
            self.stock1_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        elif self.stock2 is None or self.stock2 == 0:
            self.stock2 = stock
            self.stock2_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        elif self.stock3 is None or self.stock3 == 0:
            self.stock3 = stock
            self.stock3_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        else:
            return

        DBsession.merge(self)
        self.commit()


class AmzUserTrackedAsinKeyword(Base, BaseMethod):
    __tablename__ = 'amz_user_tracked_asin_keywords'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    market_place_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    keywords = Column(VARCHAR(512), nullable=False)
    group_desc = Column(VARCHAR(128), default='aps')

    _QUERY_DISTINCT_KEYWORDS_GROUP = '''
    SELECT keywords, group_desc, count(0) FROM
    amz_user_tracked_asin_keywords
    WHERE market_place_id = %d
    GROUP BY keywords, group_desc;
    '''

    _QUERY_DISTINCT_ALL_KEYWORDS_GROUP = '''
    SELECT keywords, group_desc, market_place_id, count(0) FROM
    amz_user_tracked_asin_keywords
    GROUP BY keywords, group_desc, market_place_id;
    '''

    @classmethod
    def query_only_by_userid(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def query_by_userid(cls, user_id, market_place_id):
        return DBsession.query(cls).filter(
            cls.user_id == user_id,
            cls.market_place_id == market_place_id).all()

    @classmethod
    def query_by_userid_all(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def query_by_userid_asin(cls, user_id, market_place_id, asin):
        return DBsession.query(cls).filter(
            cls.user_id == user_id,
            cls.market_place_id == market_place_id,
            cls.asin == asin).all()

    @classmethod
    def query_all_tracked_keywords(cls, market_place_id):
        rows = fetchall(
            cls._QUERY_DISTINCT_KEYWORDS_GROUP % market_place_id)

        return [(row[0], row[1])
                for row in rows]

    @classmethod
    def get_all_tracked_keywords(cls):
        rows = fetchall(cls._QUERY_DISTINCT_ALL_KEYWORDS_GROUP)

        return [(row[0], row[1], row[2])
                for row in rows]

    @classmethod
    def query_by_userid_asin_keywords(cls, user_id, market, asin, keywords,
                                      group_desc):
        return DBsession.query(cls).filter(
            cls.user_id == user_id,
            cls.market_place_id == market,
            cls.asin == asin,
            cls.group_desc == group_desc,
            cls.keywords == keywords).first()

    @classmethod
    def query_by_asin_keywords(cls, market, asin, keywords):
        return DBsession.query(cls).filter(
            cls.market_place_id == market,
            cls.asin == asin,
            cls.keywords == keywords).first()


class AmzDiagnosedAsinInfo(Base, BaseMethod):
    __tablename__ = 'amz_diagnosed_asin_infos'

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    title = Column(VARCHAR(512), nullable=False)
    image_url = Column(VARCHAR(65535), nullable=False)
    seller_cnt = Column(BIGINT, default=1)
    url_name = Column(VARCHAR(128), default='')
    seller_ranks = Column(JSONB)
    ladder = Column(VARCHAR(256), default='')
    node = Column(VARCHAR(128), default='')

    price = Column(BIGINT, default=0)
    thumb_image_url = Column(VARCHAR(512), default='')
    description = Column(VARCHAR(65535), default='')
    is_fba = Column(BOOLEAN, default=True)
    is_adult = Column(Boolean, default=False)
    brand = Column(VARCHAR(512), default='')

    __table_args__ = (Index('amz_diagnosed_asin_idx_1', 'market_place_id',
                            'asin', unique=True),)

    @classmethod
    def get_by_asin(cls, market_place_id, asin):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place_id,
            func.upper(cls.asin) == asin.upper()).first()

    @classmethod
    def get_by_asin_list(cls, asin_list):
        return DBsession.query(cls).filter(
            func.upper(cls.asin).in_(asin_list)).all()

    @classmethod
    def save(cls, market_place_id, asin, title, image_url, seller_cnt,
             seller_ranks, url_name, ladder, node, price, thumb_image_url,
             is_fba, is_adult=False, brand='', commit=True):
        obj = cls.get_by_asin(market_place_id, asin)
        if obj is None:
            obj = AmzDiagnosedAsinInfo(market_place_id=market_place_id,
                                       asin=asin,
                                       title=title,
                                       image_url=image_url,
                                       seller_cnt=seller_cnt,
                                       seller_ranks=seller_ranks,
                                       url_name=url_name,
                                       ladder=ladder,
                                       node=node,
                                       price=price,
                                       thumb_image_url=thumb_image_url,
                                       is_fba=is_fba,
                                       is_adult=is_adult,
                                       brand=brand)
            obj.add(commit=False)
        else:
            obj.title = title
            obj.image_url = image_url
            obj.seller_cnt = seller_cnt
            obj.seller_ranks = seller_ranks
            obj.url_name = url_name
            obj.ladder = ladder
            obj.node = node
            obj.price = price
            obj.thumb_image_url = thumb_image_url
            obj.is_fba = is_fba
            obj.is_adult = is_adult
            obj.brand = brand
            obj.update(commit=False)

        if commit:
            obj.commit()

    @classmethod
    def store_url_names(cls, market_place_id, result):
        for asin in result:
            obj = cls.get_by_asin(market_place_id, asin)
            if obj is None:
                continue

            if obj.url_name != result[asin] and not result[asin]:
                obj.url_name = result[asin]
                obj.update(False)

        cls.commit()


class AmzBestSellerAsinKw(Base, BaseMethod):
    __tablename__ = 'amz_best_seller_asin_kws'

    id = Column(VARCHAR(255), primary_key=True)
    marketplace_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(16), nullable=False)
    keywords = Column(VARCHAR(512), nullable=False)
    keyword_type = Column(VARCHAR(64), nullable=False)

    @classmethod
    def query_by_asin(cls, marketplace_id, asin):
        return DBsession.query(cls).filter(
            cls.marketplace_id == marketplace_id,
            func.upper(cls.asin) == asin.upper()).all()

    @classmethod
    def query_by_asin_type(cls, marketplace_id, asins, keywords_types,
                           limit=RTN_CNT):
        if not asins:
            return []
        return DBsession.query(cls).filter(
            cls.marketplace_id == marketplace_id,
            func.upper(cls.asin).in_(asins),
            cls.keyword_type.in_(keywords_types)).limit(limit).all()


class AmzBestSellerKwToAsin(Base, BaseMethod):
    __tablename__ = 'amz_best_seller_kw_to_asins'

    id = Column(VARCHAR(255), primary_key=True)
    marketplace_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(16), nullable=False)
    keywords_by_clicks_id = Column(VARCHAR(512), nullable=True)
    keywords_by_clicks_probability = Column(REAL, nullable=True)
    alias_id = Column(VARCHAR(512), nullable=True)
    alias_probability = Column(REAL, nullable=True)
    keywords_by_purchases_id = Column(VARCHAR(512), nullable=True)
    keywords_by_purchases_probability = Column(REAL, nullable=True)
    keywords_by_searches_id = Column(VARCHAR(512), nullable=True)
    keywords_by_searches_probability = Column(REAL, nullable=True)
    keywords_by_adds_id = Column(VARCHAR(512), nullable=True)
    keywords_by_adds_probability = Column(REAL, nullable=True)

    _QUERY_ADDCART_KW_BY_ASIN = '''
        SELECT keywords_by_adds_id FROM amz_best_seller_kw_to_asins
        WHERE asin IN ({asins}) AND marketplace_id = {marketplace_id}
        GROUP BY keywords_by_adds_id
        ORDER BY sum(keywords_by_adds_probability) DESC
        LIMIT {limit}
    '''

    @classmethod
    def query_addcart_keywords_by_asin(cls, marketplace_id, asins,
                                       limit=RTN_CNT):
        sql = cls._QUERY_ADDCART_KW_BY_ASIN.format(**{'asins':
                                                      '\'' + '\',\''.join(
                                                          asins) + '\'',
                                                      'marketplace_id':
                                                      marketplace_id,
                                                      'limit': limit})
        return [kw[0] for kw in fetchall(sql)]


def format_keywords(keywords):
    if not keywords:
        return ''

    tokens = re.split(';|,|\*|\+|\ |\%|\?|\n', keywords)
    return ' '.join([token for token in tokens if token]).lower()


class AmzTopQuery(Base, BaseMethod):
    __tablename__ = 'amz_top_querys'

    id = Column(VARCHAR(255), primary_key=True)
    keywords = Column(VARCHAR(512))
    rank = Column(BIGINT)
    query_groups = Column(BIGINT)
    searches = Column(BIGINT)
    click_count = Column(BIGINT)
    click_rate = Column(REAL)
    add_count = Column(BIGINT)
    add_rate = Column(REAL)
    purchase_count = Column(BIGINT)
    ops = Column(BIGINT)
    reformulation_rate = Column(REAL)
    abandonment_rate = Column(REAL)
    abandonment_rate = Column(REAL)
    click_depth = Column(REAL)
    add_depth = Column(REAL)
    month = Column(VARCHAR(16))
    group_name = Column(VARCHAR(128))
    marketplace_name = Column(VARCHAR(16))

    _SQL_TMPL = '''
        WITH top_query_tmp AS(
            SELECT
                DISTINCT keywords,
                COUNT(month) OVER (PARTITION BY keywords) AS cnt,
                SUM({field}) AS sum_field
            FROM amz_top_querys
            WHERE lower(keywords) IN ({keywords_list})
                AND marketplace_name='{market}'
                AND month in ({month_list})
                AND group_name in {group_desc}
            GROUP BY keywords, month
        )
        SELECT keywords, cnt, SUM(sum_field) AS sum_f FROM top_query_tmp
        GROUP BY keywords, cnt;
    '''

    _EXTEND_KEYWORDS_SQL = '''
    SELECT keywords, sum(similarity(keywords, $maxsonic${keywords}$maxsonic$)
    * ln(searches))
    AS cnt FROM amz_top_querys
    WHERE marketplace_name= '{market}' and month in ({month_list})
    and searches > 0
    group by keywords
    ORDER BY cnt DESC limit {limit};
    '''
    _EXTEND_KEYWORDS_SQL_WITH_GROUP_DESC = '''
    SELECT keywords, sum(similarity(keywords, $maxsonic${keywords}$maxsonic$)
    * ln(searches))
    AS cnt FROM amz_top_querys
    WHERE marketplace_name= '{market}' and month in ({month_list})
    and searches > 0 and group_name='{group_desc}'
    group by keywords
    ORDER BY cnt DESC limit {limit};
    '''

    _traffic_distribution = [
        {'from': 1, 'to': 18, 'probility': 0.8},
        {'from': 18, 'to': 36, 'probility': 0.10},
        {'from': 36, 'to': 54, 'probility': 0.07},
        {'from': 54, 'to': 300, 'probility': 0.03}]

    ADD_PROBOLITY_IMPOSSIBLE = 'IMPOSSIBLE'
    ADD_PROBOLITY_TINY = 'TINY'
    ADD_PROBOLITY_SMALL = 'SMALL'
    ADD_PROBOLITY_NORMAL = 'NORMAL'
    ADD_PROBOLITY_GOOD = 'GOOD'
    TRAFFIC_LEVEL_BAD = 0
    TRAFFIC_LEVEL_NORMAL = 1
    TRAFFIC_LEVEL_BETTER = 2
    TRAFFIC_LEVEL_BEST = 3

    _TQ_HAS_MONTH_DATA_SQL = '''
    SELECT * FROM amz_top_querys WHERE marketplace_name = '{market}'
    AND month = '{month}' LIMIT 1
    '''

    @classmethod
    def check_one_amz_top_query(cls, market, last_month):
        test_sql = cls._TQ_HAS_MONTH_DATA_SQL.format(**{'market': market,
                                                        'month': last_month})
        return fetchall(test_sql)

    @classmethod
    def get_extend_keywords(cls, market, keywords, month_list=None, limit=5):
        marketplace_name = AmzMarketplace.get(market).market_place
        if month_list is None:
            dt = datetime.utcnow()
            last_month = str(make_last_month_period())
            test_result = cls.check_one_amz_top_query(marketplace_name,
                                                      last_month)
            if not test_result:
                month_list =\
                    make_month_before_last_month_period(return_list=True)
            else:
                month_list = [last_month,
                              str(make_last_year_month_period(dt))]

        sql = cls._EXTEND_KEYWORDS_SQL.format(**{'keywords': keywords.lower(),
                                                 'market': marketplace_name,
                                                 'month_list':
                                                 '\'' + '\',\''.join(
                                                     month_list) + '\'',
                                                 'limit': limit})

        return fetchall(sql)

    @classmethod
    def get_extend_keywords_with_group_desc(cls, market, keywords, group_desc,
                                            month_list=None, limit=5):
        marketplace_name = AmzMarketplace.get(market).market_place
        if month_list is None:
            dt = datetime.utcnow()
            last_month = str(make_last_month_period())
            test_result = cls.check_one_amz_top_query(marketplace_name,
                                                      last_month)
            if not test_result:
                month_list =\
                    make_month_before_last_month_period(return_list=True)
            else:
                month_list = [last_month,
                              str(make_last_year_month_period(dt))]
        sql = cls._EXTEND_KEYWORDS_SQL_WITH_GROUP_DESC.format(
            **{'keywords': keywords.lower(), 'market': marketplace_name,
               'month_list': '\'' + '\',\''.join(month_list) + '\'',
               'limit': limit, 'group_desc': group_desc.upper()})

        return fetchall(sql)

    @classmethod
    def _get_kw_data(cls, market, keywords_list, group_desc=DEFAULT_GROUP_DESC,
                     field="searches", month_list=None):
        kws_map = {kw: format_keywords(kw) for kw in keywords_list}
        kw_list = [kw.lower() for kw in kws_map.values() if kw]
        dt = datetime.utcnow()
        if month_list is None:
            last_month = str(make_last_month_period())
            test_result = cls.check_one_amz_top_query(market, last_month)
            if not test_result:
                month_list =\
                    make_month_before_last_month_period(return_list=True)
            else:
                month_list = [last_month,
                              str(make_last_year_month_period(dt))]
        data = {'field': field,
                'keywords_list': '$maxsonic$' + '$maxsonic$,$maxsonic$'.
                join(kw_list) + '$maxsonic$',
                'market': market,
                'group_desc': group_desc if group_desc.upper()
                else DEFAULT_GROUP_DESC,
                'month_list': '\'' + '\',\''.join(month_list) + '\''}
        sql = cls._SQL_TMPL.format(**data)
        rows = fetchall(sql)
        score_list = {row.keywords: row.sum_f/row.cnt if row.cnt != 0 else 0
                      for row in rows}

        return {k: float(score_list.get(v, 0)) for k, v in kws_map.iteritems()}

    @classmethod
    def get_kw_add_count(cls, market, keywords,
                         group_desc=DEFAULT_GROUP_DESC, month_list=None):
        result = cls._get_kw_data(market, [keywords], group_desc,
                                  'add_count', month_list)
        if not result:
            return 0

        return result[keywords] if keywords in result else 0

    @classmethod
    def get_kw_add_prob(cls, market, keywords, keywords_ranking,
                        month_list=None):
        def _get_traffic_probility(ranking):
            for traffic in cls._traffic_distribution:
                if ranking >= traffic['from'] and ranking < traffic['to']:
                    return traffic['probility']

            return 0

        def _get_add_probility(score):
            if score < 0.1:
                return cls.ADD_PROBOLITY_IMPOSSIBLE
            elif score >= 0.1 and score < 5:
                return cls.ADD_PROBOLITY_TINY
            elif score >= 5 and score < 25:
                return cls.ADD_PROBOLITY_SMALL
            elif score >= 25 and score < 125:
                return cls.ADD_PROBOLITY_NORMAL
            elif score >= 125:
                return cls.ADD_PROBOLITY_GOOD

        if keywords_ranking >= 300:
            return cls.ADD_PROBOLITY_IMPOSSIBLE

        add_count = cls.get_kw_add_count(market, keywords, DEFAULT_GROUP_DESC,
                                         month_list)
        score = add_count * _get_traffic_probility(keywords_ranking)
        return _get_add_probility(score)

    @classmethod
    def get_kw_list_search(cls, market, keywords_list,
                           group_desc=DEFAULT_GROUP_DESC, month_list=None):
        return cls._get_kw_data(market, keywords_list, group_desc,
                                'searches', month_list)

    @classmethod
    def get_traffic_level(cls, traffic):
        if traffic < 5000:
            return cls.TRAFFIC_LEVEL_BAD
        elif traffic >= 5000 and traffic < 20000:
            return cls.TRAFFIC_LEVEL_NORMAL
        elif traffic >= 20000 and traffic < 100000:
            return cls.TRAFFIC_LEVEL_BETTER
        elif traffic >= 100000:
            return cls.TRAFFIC_LEVEL_BEST

    @classmethod
    def get_by_market_month(cls, market, month_period):
        return DBsession.query(cls).\
            filter(cls.marketplace_name == market,
                   cls.month == month_period).all()


class AmzBestSellerPage(Base, BaseMethod):
    __tablename__ = 'amz_best_seller_pages'
    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    url = Column(VARCHAR(256), nullable=False, unique=True)

    @classmethod
    def get_by_market_place_id(cls, market):
        return DBsession.query(cls).filter(cls.market_place_id == market).all()

    @classmethod
    def get_by_node(cls, node, market):
        return DBsession.query(cls).filter(cls.url.like('%' + node),
                                           cls.market_place_id == market).\
            first()


class AmzBestSellerUrl(Base, BaseMethod):
    __tablename__ = 'amz_best_seller_urls'
    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    category = Column(VARCHAR(128))
    url = Column(VARCHAR(256), nullable=False)
    pid = Column(BIGINT, default=0)
    page_id = Column(BIGINT, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    update_at = Column(TIMESTAMP(timezone=True))
    __table_args__ = (Index('amz_best_seller_urls_idx', 'market_place_id',
                            'category', 'url', 'pid', unique=True),)
    SQL_GET_TREE_BY_ID = '''
        WITH RECURSIVE first_level_elements AS
    (
        SELECT url, id, market_place_id
        FROM amz_best_seller_urls
        WHERE amz_best_seller_urls.id = :cid
        AND amz_best_seller_urls.market_place_id = :market_id
    UNION
        SELECT q.url, q.id, q.market_place_id
        FROM first_level_elements fle, amz_best_seller_urls q
        WHERE fle.id = q.pid
    )
    SELECT * from first_level_elements;
    '''

    def update(self, commit=True):
        self.update_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        DBsession.merge(self)
        if commit:
            self.commit()

    def add(self, commit=True):
        self.create_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        DBsession.add(self)
        if commit:
            self.commit()

    @classmethod
    def get_tree_by_id(cls, cid, market_id):
        return fetchall(cls.SQL_GET_TREE_BY_ID, {'cid': cid,
                                                 'market_id': market_id})

    @classmethod
    def get_by_category(cls, category):
        return DBsession.query(cls).filter(cls.category == category).all()

    @classmethod
    def get_by_market_place_id(cls, market_place_id):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id).all()

    @classmethod
    def get_by_url(cls, url):
        return DBsession.query(cls).filter(cls.url == url).scalar()

    @classmethod
    def get_by_category_pid(cls, category, pid, mid):
        return DBsession.query(cls).filter(cls.pid == pid,
                                           cls.category == category,
                                           cls.market_place_id == mid).first()

    def to_json(self):
        return {'id': self.id,
                'category': self.category}


class AmzBestSeller(Base, BaseMethod):
    __tablename__ = 'amz_best_sellers'
    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    category_id = Column(BIGINT, nullable=False)
    rank_number = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(16), nullable=False)
    title = Column(VARCHAR(512))
    search_title = Column(VARCHAR(512))
    document = Column(TSVECTOR)
    price_min = Column(REAL, default=0)
    price_max = Column(REAL, default=0)
    review_count = Column(BIGINT, default=0)
    review_rate = Column(REAL, default=0)
    offer_count = Column(BIGINT, default=0)
    offer_price_min = Column(REAL, default=0)
    offer_price_max = Column(REAL, default=0)
    create_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    SQL_QUERY_URL = '''
    SELECT url FROM amz_best_sellers GROUP BY url
    '''

    def add(self, commit=True):
        self.create_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        DBsession.add(self)
        if commit:
            self.commit()

    @classmethod
    def get_by_asin_market(cls, asin, market):
        return DBsession.query(cls).filter(cls.asin == asin,
                                           cls.market_place_id == market).all()

    @classmethod
    def get_urls(cls):
        return fetchall(cls.SQL_QUERY_URL)

    @classmethod
    def get_by_category_id(cls, category_id, rank_num=3):
        return DBsession.query(cls).filter(cls.category_id == category_id,
                                           cls.rank_number <= rank_num).\
            order_by(func.to_char(cls.create_at, 'YYYYMM').desc(),
                     cls.rank_number).limit(10).all()

    @classmethod
    def get_by_title(cls, market, title, limit=RTN_CNT):
        lang_map = {1: 'english', 3: 'english', 7: 'english', 4: 'german',
                    5: 'french', 35691: 'italian', 44551: 'spanish'}
        rank_sql = '''
        SELECT asin
        FROM (SELECT
            amz_best_sellers.market_place_id  as market_place_id,
            amz_best_sellers.asin as asin,
            document
            FROM amz_best_sellers) p_search
        WHERE p_search.document @@ to_tsquery('%s', $maxsonic$%s$maxsonic$)
        and market_place_id=%d
        ORDER BY ts_rank(p_search.document, to_tsquery('%s',
        $maxsonic$%s$maxsonic$)) DESC LIMIT %d;
        '''
        change_conf = "SET default_text_search_config = " + \
            "'pg_catalog.%s';" % lang_map[market]
        DBsession.execute(change_conf)
        p = re.compile('\W+')
        final_title = ' | '.join(p.split(title)[:TITLE_LIMIT])

        execute_sql = rank_sql % (lang_map[market], final_title, market,
                                  lang_map[market], final_title, limit)
        result = fetchall(execute_sql)
        return [asin[0] for asin in result] if result else None

    def to_json(self):
        return {'id': self.id,
                'rank_number': self.rank_number,
                'asin': self.asin,
                'create_at': make_date_period(self.create_at)}


class ECSPAmzMailTmpl(Base, BaseMethod):
    ACTIVE_ACCOUNT = 1
    FORGET_PASSWORD = 2
    UPDATE_VERSION = 3
    REMIND_ACCOUNT = 4
    CHANGE_PLAN = 5
    CHANGE_PASSWORD = 6
    SRV_CHARGE_CREDIT = 7
    __tablename__ = 'ecsp_amz_mail_tmpls'
    id = Column(BIGINT, primary_key=True)
    subject = Column(VARCHAR(255), nullable=False)
    msg = Column(VARCHAR(65535))
    typ = Column(BIGINT, nullable=False)
    tmpl_str = Column(VARCHAR(64))

    @classmethod
    def get_by_type(cls, typ):
        return DBsession.query(cls).filter(cls.typ == typ).first()

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return

        mail_tmpl_data = [
            {"subject": "帐号激活",
             "msg": "请点击以下链接激活帐号: %s",
             "typ": 1, "tmpl_str": "template_activateaccount"},
            {"subject": "重置密码", "msg": "验证码为 %s",
             "typ": 2, "tmpl_str": "template_resetpassword"},
            {"subject": "版本更新", "msg": "新版本号为 %s",
             "typ": 3, "tmpl_str": "template_updateversion"},
            {"subject": "余额提醒",
             "msg": '''您当前账户排名提升的余额为%d， 近期日均消耗为%d。
             为避免余额不足导致排名提升功能不能正常使用，请及时充值。''',
             "typ": 4, "tmpl_str": "template_remindaccount"},
            {"subject": "套餐修改", "msg": "您的套餐已经修改为 %s",
             "typ": 5, "tmpl_str": "template_changeplan"},
            {"subject": "密码修改",
             "msg": "您的密码已被 %s 修改， 请确认是您本人进行的修改。",
             "typ": 6, "tmpl_str": "template_changepassword"},
            {"subject": "排名提升服务充值成功",
             "msg": "您已成功充值关键词排名提升服务 %d 点。截至目前，您当前账户排名提升余额为 %d 点。",
             "typ": 7, "tmpl_str": "template_kw_impr_charge_credit"}]

        for data in mail_tmpl_data:
            mail_tmp = ECSPAmzMailTmpl(
                subject=data.get('subject'), msg=data.get('msg'),
                typ=data.get('typ'), tmpl_str=data.get('tmpl_str'))
            mail_tmp.add(commit=False)
        cls.commit()


class ECSPAmzWechatTmpl(Base, BaseMethod):
    WECHAT_QUOTA_REMINDER = 1
    WECHAT_SRV_CHARGE_CREDIT = 2
    __tablename__ = 'ecsp_amz_wechat_tmpls'
    id = Column(BIGINT, primary_key=True)
    wechat_tmpl_data = Column(VARCHAR(65535))
    typ = Column(BIGINT, nullable=False)
    tmpl_id = Column(VARCHAR(64))

    @classmethod
    def get_by_type(cls, typ):
        return DBsession.query(cls).filter(cls.typ == typ).first()

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return

        remind_tmpl_data = {
            "first": {
                "value": "尊敬的VIP客户，您的排名提升余额即将不足",
                "color": "#173177"
                },
            "keyword1": {
                "value": "%s(%s)",
                "color": "#173177"
                },
            "keyword2": {
                "value": "%d点",
                "color": "#173177"
                },
            "remark": {
                "value": "您的日均消耗为%d点，感谢您使用电商助手Oceanus",
                "color": "#173177"
                },
            }
        charge_tmpl_data = {
            "first": {
                "value": "尊敬的VIP客户，您的排名提升充值已到账",
                "color": "#173177"
                },
            "keyword1": {"value": "%s(%s)", "color": "#173177"},
            "keyword2": {"value": "%d点", "color": "#173177"},
            "remark": {
                "value": "截至目前，您的账户余额为%d点，感谢您使用电商助手Oceanus",
                "color": "#173177"
                }
            }
        wechat_tmpl_data = [
            {"wechat_tmpl_data": json.dumps(OrderedDict(
                sorted(remind_tmpl_data.items(), key=lambda t: t[0]))),
             "typ": 1,
             "tmpl_id": "jaz20X5hcxmR28lkPqRNKBiXQB_FDp8HNR0YFSmm3c4"},
            {"wechat_tmpl_data": json.dumps(OrderedDict(
                sorted(charge_tmpl_data.items(), key=lambda t: t[0]))),
             "typ": 2,
             "tmpl_id": "Lu6NhR4zoxCGBuabveZFw3kjs4qE-vykB6W8PzfiHuU"}]

        for data in wechat_tmpl_data:
            wechat_tmpl = ECSPAmzWechatTmpl(
                wechat_tmpl_data=data.get('wechat_tmpl_data'),
                typ=data.get('typ'), tmpl_id=data.get('tmpl_id'))
            wechat_tmpl.add(commit=False)
        cls.commit()


class ECSPAmzServiceChargeLog(Base, BaseMethod):
    __tablename__ = 'ecsp_amz_service_charge_logs'
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    service_id = Column(BIGINT, default=7)
    price = Column(BIGINT, default=0)
    quota = Column(BIGINT, default=0)
    promotion_quota = Column(BIGINT, default=0)
    operator = Column(VARCHAR(64))
    comment = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class ECSPAmzMail(Base, BaseMethod):
    __tablename__ = 'ecsp_amz_mails'
    id = Column(BIGINT, primary_key=True)
    subject = Column(VARCHAR(255), nullable=False)
    message = Column(VARCHAR(65535))
    user_id = Column(BIGINT, nullable=False)
    typ = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_by_user_id_n_type(cls, user_id, typ):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.typ == typ).all()

    @classmethod
    def delete_mail_by_type(cls, user_id, typ):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.typ == typ).delete()

    @classmethod
    def get_new_mails_by_userid(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.updated_at.is_(None)).all()

    @classmethod
    def set_read_flag_by_id(cls, mail_id, commit=True):
        obj = ECSPAmzMail.get_by_id(mail_id)
        if not obj:
            return

        obj.updated_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        obj.update(commit)

    @classmethod
    def delete_by_id(cls, mail_id, commit=True):
        obj = ECSPAmzMail.get_by_id(mail_id)
        obj.delete(commit)


class ECSPAmzGroup(Base, BaseMethod):
    __tablename__ = 'ecsp_amz_groups'
    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, primary_key=True)
    group_on_ui = Column(VARCHAR(255), nullable=False)
    group_best_seller = Column(VARCHAR(255), nullable=False)
    group_on_db = Column(VARCHAR(1024), nullable=False)

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return

        from models.ecsp_amz_group import get_amz_map_group
        from models.ecsp_amz_group import get_amz_map_group
        ecsp_amz_marketplace_group_map = get_amz_map_group(return_all=True,
                                                           marketplace='None')

        for market_place in ecsp_amz_marketplace_group_map.keys():
            market = AmzMarketplace.get_by_market_place(market_place)
            group_alias = ecsp_amz_marketplace_group_map[market_place][0]
            group_map = ecsp_amz_marketplace_group_map[market_place][1]
            for group_key in group_alias.keys():
                amz_group = ECSPAmzGroup(
                    market_place_id=market.id,
                    group_on_ui=group_alias[group_key],
                    group_best_seller=group_key,
                    group_on_db=group_map[group_key])
                DBsession.add(amz_group)

        try:
            DBsession.commit()
        except Exception:
            DBsession.rollback()

    @classmethod
    def get_by_market_place_id(cls, market_place):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place).all()

    @classmethod
    def get_by_market_from_ui(cls, market_place, ui):
        return DBsession.query(cls).filter(
            cls.market_place_id == market_place,
            cls.group_on_ui == ui).first()

    def to_json(self):
        return {'group_on_ui': self.group_on_ui,
                'group_best_seller': self.group_best_seller}


class AmzAccountInfo(Base, BaseMethod):
    __tablename__ = 'amz_account_infos'
    NORMAL_ACCOUNT = 1
    FARM_ACCOUNT = 2
    TEST_ACCOUNT = 999

    id = Column(BIGINT, primary_key=True)
    market_place_id = Column(BIGINT, nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    password = Column(VARCHAR(64), nullable=False)
    given_name = Column(VARCHAR(64), nullable=False)
    surname = Column(VARCHAR(64), nullable=False)
    addr_state = Column(VARCHAR(16), nullable=False)
    addr_state_full = Column(VARCHAR(128))
    addr_city = Column(VARCHAR(64), nullable=False)
    addr_street = Column(VARCHAR(256), nullable=False)
    zip_code = Column(VARCHAR(16), nullable=False)
    telephone = Column(VARCHAR(32), nullable=False)
    last_used = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    ua = Column(VARCHAR(256), default='')
    account_type = Column(BIGINT, default=NORMAL_ACCOUNT)
    bind_proxy_id = Column(BIGINT, default=0)
    balance = Column(BIGINT, default=0)
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
                               account_type=NORMAL_ACCOUNT,
                               is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.account_type == account_type,
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
                'telephone': self.telephone,
                'ua': self.ua,
                'last_used': str(self.last_used),
                'account_type': self.account_type,
                'bind_proxy_id': self.bind_proxy_id,
                'balance': self.balance,
                'is_available': self.is_available}

    @classmethod
    def query_by_marketplace_limit(cls, market_place_id, limit=50,
                                   account_type=NORMAL_ACCOUNT,
                                   is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.account_type == account_type,
                   cls.is_available == is_available).\
            order_by(cls.last_used).limit(limit).all()

    @classmethod
    def query_by_limit(cls, limit=50, account_type=NORMAL_ACCOUNT,
                       is_available=True):
        return DBsession.query(cls).\
            filter(cls.account_type == account_type,
                   cls.is_available == is_available).\
            order_by(cls.last_used).limit(limit).all()

    @classmethod
    def query_by_marketplace_days_ago(cls, market_place_id, days=7,
                                      account_type=NORMAL_ACCOUNT,
                                      is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.last_used <= datetime.utcnow() - timedelta(days=days),
                   cls.account_type == account_type,
                   cls.is_available == is_available).\
            all()

    @classmethod
    def query_unbind_account(cls, market_place_id, account_type=FARM_ACCOUNT,
                             is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.account_type == account_type,
                   cls.bind_proxy_id == 0,
                   cls.is_available == is_available).all()

    @classmethod
    def query_binding_account(cls, market_place_id, account_type=FARM_ACCOUNT,
                              is_available=True):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_place_id,
                   cls.account_type == account_type,
                   cls.is_available == is_available,
                   cls.bind_proxy_id > 0).all()

    @classmethod
    def bind_ip_to_account(cls, market_place_id, account_type=FARM_ACCOUNT,
                           bind_account_count=5):

        def _bind(accounts, proxy_ip, need_account):
            for acct in accounts:
                if proxy_ip.bind_account_count == need_account:
                    return
                acct.bind_proxy_id = proxy_ip.id
                proxy_ip.bind_account_count += 1

        accounts = cls.query_unbind_account(market_place_id)
        proxy_ips = ECSPPrivateProxy.query_valid_farm_proxies()
        if not proxy_ips or not accounts:
            return True

        accounts_len = len(accounts)
        acct_index = 0

        for proxy_ip in proxy_ips:
            need_account = bind_account_count - proxy_ip.bind_account_count
            _bind(accounts[acct_index:], proxy_ip, need_account)
            acct_index += need_account
            if acct_index >= accounts_len:
                break
        return BaseMethod.commit()

    @classmethod
    def unbind_ip_to_account(cls, market_place_id, proxy_list,
                             account_type=FARM_ACCOUNT):
        for proxy in proxy_list:
            accounts = DBsession.query(cls).\
                filter(cls.market_place_id == market_place_id,
                       cls.account_type == account_type,
                       cls.bind_proxy_id == proxy.id).all()
            for acct in accounts:
                acct.bind_proxy_id = 0
                proxy.bind_account_count -= 1 if\
                    proxy.bind_account_count > 0 else 0
        return BaseMethod.commit()

    def use(self, commit=True):
        self.last_used = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.update(commit)

    def soft_delete(self, commit=True):
        self.is_available = False
        self.update(commit)

    @classmethod
    def is_account_available(cls, account_id):
        account = AmzAccountInfo.get_by_id(account_id)
        return account and account.is_available


class AmzFailAccountLog(Base, BaseMethod):
    __tablename__ = 'amz_fail_account_logs'

    id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, nullable=False)
    market_place_id = Column(BIGINT, nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class ECSPRealAddress(Base, BaseMethod):
    __tablename__ = 'ecsp_real_addresses'

    id = Column(BIGINT, primary_key=True)
    country = Column(VARCHAR(64), nullable=False)
    state = Column(VARCHAR(16), nullable=False)
    state_full = Column(VARCHAR(128))
    city = Column(VARCHAR(64), nullable=False)
    address_line1 = Column(VARCHAR(256), nullable=False)
    address_line2 = Column(VARCHAR(256))
    zip_code = Column(VARCHAR(16), nullable=False)

    @classmethod
    def get_any_by_country(cls, country):
        return choice(DBsession.query(cls).
                      filter(cls.country == country).all())

    @classmethod
    def get_any(cls):
        return choice(cls.get_all())

    def to_json(self):
        return {'address_line1': self.address_line1,
                'address_line2': self.address_line2,
                'country': self.country,
                'city': self.city,
                'state': self.state,
                'state_full': self.state_full,
                'zip_code': self.zip_code}


class AmzKwRankImprPrj(Base, BaseMethod):
    __tablename__ = 'amz_kw_rank_impr_prjs'

    # XXX: it shall use the foreign key of AmzUserTrackedAsinKeyword
    #      however the business deceision is not finilized, and it is possible
    #      to be a standalone tool. so I have to duplicate all the fields.
    #
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    market_place_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    keywords = Column(VARCHAR(512), nullable=False)
    quantity = Column(BIGINT, default=50)
    is_accelerated = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    target_ranking = Column(BIGINT, default=15)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)
    manual_quantity = Column(BIGINT, nullable=False, default=0)
    is_random_prj = Column(BOOLEAN, default=False)
    impr_type = Column(BIGINT)
    group_desc = Column(VARCHAR(128), default='aps')

    __DEFAULT_QUANTITY = 25
    CART_FARMING = 1
    DYNAMIC_SUPERURL = 2
    WISH_LIST = 3

    @classmethod
    def get_default_quantity(cls):
        return cls.__DEFAULT_QUANTITY

    @classmethod
    def get_market_active(cls, market_id):
        return DBsession.query(cls).filter(cls.market_place_id == market_id,
                                           cls.is_active == true()).all()

    @classmethod
    def get_market_user_active(cls, user_id, market_id):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.market_place_id == market_id,
                                           cls.is_active == true()).all()

    @classmethod
    def get_by_user_asin_kws(cls, user_id, market_id, asin, keywords,
                             group_desc='aps'):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.market_place_id == market_id,
                                           cls.asin == asin,
                                           cls.group_desc == group_desc,
                                           cls.keywords == keywords).all()

    @classmethod
    def get_by_user_asin_kws_type_group(cls, user_id, market_id, asin,
                                        keywords, impr_type, group_desc='aps'):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.market_place_id == market_id,
                                           cls.asin == asin,
                                           cls.keywords == keywords,
                                           cls.group_desc == group_desc,
                                           cls.impr_type == impr_type).first()

    @classmethod
    def get_act_prj_by_user_asin_kws(cls, user_id, market_id, asin, keywords):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.market_place_id == market_id,
                                           cls.asin == asin,
                                           cls.keywords == keywords,
                                           cls.is_active == true()).first()

    def on_start(self, commit=True):
        prj_log = AmzKwRankImprPrjLog.\
            get_last_started_log(self.user_id, self.market_place_id, self.asin,
                                 self.keywords, self.impr_type,
                                 self.group_desc)
        if not prj_log:

            AmzKwRankImprPrjLog(user_id=self.user_id,
                                market_place_id=self.market_place_id,
                                asin=self.asin, keywords=self.keywords,
                                quantity=self.quantity,
                                is_accelerated=self.is_accelerated,
                                state=AmzKwRankImprPrjLog.START,
                                group_desc=self.group_desc,
                                impr_type=self.impr_type).add(False)
        return True if not commit else BaseMethod.commit()

    def on_stop(self, commit=True):
        prj_log = AmzKwRankImprPrjLog.\
            get_last_started_log(self.user_id, self.market_place_id, self.asin,
                                 self.keywords, self.impr_type,
                                 self.group_desc)
        if prj_log:
            prj_log.stop(False)
        return True if not commit else BaseMethod.commit()

    def stop(self):
        self.is_active = False
        self.is_accelerated = False
        self.update(False)
        return self.on_stop(True)

    def start(self, is_accelerated):
        if self.is_active:
            return True
        self.is_active = True
        self.is_accelerated = is_accelerated
        self.update(False)
        return self.on_start(True)

    def is_met_target(self):
        kw_ranking_info =\
            AmzKeywordsRanking.query_by_keywords_latest(self.market_place_id,
                                                        self.keywords,
                                                        self.group_desc)
        if not kw_ranking_info:
            return False

        asin_ranking = kw_ranking_info.get_asin_ranking(self.asin)
        if not asin_ranking:
            return False

        latest_ranking = asin_ranking.values()[0]
        return latest_ranking >= 0 and self.target_ranking >= latest_ranking

    @classmethod
    def make_task_quantity(cls, market_id, keywords, is_accelerated,
                           impr_type):
        market = AmzMarketplace.get_by_id(market_id)
        if impr_type == cls.CART_FARMING:
            qty = AmzTopQuery.get_kw_add_count(market=market.market_place,
                                               keywords=keywords)
        # TODO::determine the quantity
        elif impr_type == cls.WISH_LIST:
            qty = cls.__DEFAULT_QUANTITY
        else:
            qty = AmzTopQuery.get_kw_list_search(
                market=market.market_place,
                keywords_list=[keywords])[keywords]
        return min(max(int(qty)/200 if not is_accelerated else int(qty)/100,
                   cls.get_default_quantity()), 500)

    def get_daily_planned_quantity(self):
        if not self.is_met_target():
            # For special users, Magnum did this
            if self.user_id == 24:
                return 15

            if self.manual_quantity and self.manual_quantity > 0:
                return self.manual_quantity
            quantity = self.make_task_quantity(self.market_place_id,
                                               self.keywords,
                                               self.is_accelerated,
                                               self.impr_type)
            if self.quantity != quantity:
                self.quantity = quantity
                self.update()
            return quantity

        return min(self.quantity / 3, self.__DEFAULT_QUANTITY)

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()


class AmzKwRankImprDailyPrjLog(Base, BaseMethod):
    __tablename__ = 'amz_kw_rank_impr_daily_prj_logs'

    __SQL_DAILY_STAT = '''
    UPDATE amz_kw_rank_impr_daily_prj_logs
    SET actual_count = COALESCE((
        SELECT SUM(count) FROM amz_kw_rank_impr_daily_detail_logs AS detail
        WHERE detail.date_period = amz_kw_rank_impr_daily_prj_logs.date_period
        AND detail.prj_id = amz_kw_rank_impr_daily_prj_logs.prj_id
        AND detail.date_period={date_period}), 0)

    '''

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT, ForeignKey('amz_kw_rank_impr_prjs.id'))
    date_period = Column(BIGINT, default=make_date_period)
    actual_count = Column(BIGINT, default=0)

    @classmethod
    def get_by_prj_date(cls, prj_id, date_period=None):
        if date_period is None:
            date_period = make_date_period()

        return DBsession.query(cls).\
            filter(cls.prj_id == prj_id,
                   cls.date_period == date_period).first()

    @classmethod
    def bulk_add(cls, prj_ids, commit=True):
        if not prj_ids:
            return

        for prj_id in prj_ids:
            cls(prj_id=prj_id).add(commit)

    @classmethod
    def gen_daily_result(cls, date_period=None):
        '''
        It will calculate the statistic data on last day by default.
        Or calculate the data on a specific date
        '''
        if not date_period:
            date_period = make_date_period(
                datetime.utcnow() - timedelta(days=1))
        DBsession.execute(
            cls.__SQL_DAILY_STAT.format(**{'date_period': date_period}))
        cls.commit()


class AmzKwRankImprDailyAccountLog(Base, BaseMethod):
    __tablename__ = 'amz_kw_rank_impr_daily_account_logs'

    _STATUS_PENDING = 1
    _STATUS_STARTED = 2
    _STATUS_DONE = 3

    id = Column(BIGINT, primary_key=True)
    date_period = Column(BIGINT, default=make_date_period)
    account_id = Column(BIGINT, ForeignKey('amz_account_infos.id'))
    status = Column(BIGINT, default=_STATUS_PENDING)
    market_place_id = Column(BIGINT)
    params = Column(JSONB)
    scheduled_at = Column(BIGINT)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    @classmethod
    def get_by_date(cls, date_period=None):
        if not date_period:
            date_period = make_date_period()

        return DBsession.query(cls).\
            filter(cls.date_period == date_period).all()

    @classmethod
    def get_by_account_date(cls, account_id, date_period=None):
        if date_period is None:
            date_period = make_date_period()

        return DBsession.query(cls).\
            filter(cls.account_id == account_id,
                   cls.date_period == date_period).first()

    @classmethod
    def bulk_add(cls, account_ids, commit=True):
        if not account_ids:
            return

        for account_id in account_ids:
            cls(account_id=account_id).add(commit)

    def replace_account(self, commit=True):
        amz_accounts = AmzAccountInfo.query_by_limit(1)
        if not amz_accounts or len(amz_accounts) == 0:
            log.error('ERROR: Not enough amazon accounts')
            return False

        amz_accounts[0].use(False)
        self.account_id = amz_accounts[0].id
        return self.update(commit)

    def start(self):
        self.status = self._STATUS_STARTED
        self.update()

    def done(self):
        self.status = self._STATUS_DONE
        self.update()

    def is_pending(self):
        return self.status == self._STATUS_PENDING

    def is_done(self):
        return self.status == self._STATUS_DONE


class AmzSeoFailureLog(Base, BaseMethod):
    __tablename__ = 'amz_seo_failure_logs'

    id = Column(BIGINT, primary_key=True)
    date_period = Column(BIGINT, default=make_date_period)
    market_place_id = Column(BIGINT)
    account_id = Column(BIGINT, ForeignKey('amz_account_infos.id'))
    params = Column(JSONB)
    has_kicked_off = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    __table_args__ = (Index('amz_seo_failure_logs_unique_idx',
                            'date_period', 'market_place_id', 'account_id',
                            unique=True),)

    @classmethod
    def get_by_date(cls, date_period=None):
        if not date_period:
            date_period = make_date_period()

        return DBsession.query(cls).\
            filter(cls.date_period == date_period).all()

    @classmethod
    def del_by_market_account_date(cls, market_id, account_id, date_period):
        return DBsession.query(cls).\
            filter(cls.market_place_id == market_id,
                   cls.date_period == date_period,
                   cls.account_id == account_id).delete()

    def kick_off(self, commit=True):
        self.has_kicked_off = True
        self.update(commit=commit)

    def replace_account(self, account_id, commit=True):
        self.account_id = account_id
        self.update(commit=commit)


class AmzKwRankImprDailyDetailLog(Base, BaseMethod):
    __tablename__ = 'amz_kw_rank_impr_daily_detail_logs'

    id = Column(BIGINT, primary_key=True)
    date_period = Column(BIGINT, default=make_date_period)
    account_log_id =\
        Column(BIGINT, ForeignKey('amz_kw_rank_impr_daily_account_logs.id'))
    prj_id = Column(BIGINT, ForeignKey('amz_kw_rank_impr_prjs.id'))
    count = Column(BIGINT, default=0)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    __table_args__ = (Index('amz_kw_rank_impr_daily_detail_logs_idx_01',
                            'date_period', 'account_log_id', 'prj_id',
                            unique=True),)

    @classmethod
    def get_by_accountlog(cls, account_log_id, date_period=None, count=0):
        if not date_period:
            date_period = make_date_period()

        return DBsession.query(cls).\
            filter(cls.account_log_id == account_log_id, cls.count == count,
                   cls.date_period == date_period).all()

    @classmethod
    def get_by_accountlog_prj(cls, account_log_id, prj_id, date_period=None):
        if not date_period:
            date_period = make_date_period()

        return DBsession.query(cls).\
            filter(cls.account_log_id == account_log_id, cls.prj_id == prj_id,
                   cls.date_period == date_period).first()

    @classmethod
    def get_or_create(cls, account_log_id, prj_id, date_period=None):
        if not date_period:
            date_period = make_date_period()
        detail_log = cls.get_by_accountlog_prj(account_log_id, prj_id,
                                               date_period)
        if not detail_log:
            detail_log = AmzKwRankImprDailyDetailLog(
                date_period=date_period, account_log_id=account_log_id,
                prj_id=prj_id)
            detail_log.add()

        return detail_log

    def is_done(self):
        return self.count == 1

    def done(self):
        self.count = 1
        self.update()


class EcspRole(Base, BaseMethod):
    __tablename__ = 'ecsp_roles'

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)

    @classmethod
    def get_by_name(cls, name):
        return DBsession.query(cls).filter(cls.name == name).first()

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return

        all_roles = [{'id': 1, 'name': 'free'}, {'id': 2, 'name': 'vip'}]
        for data in all_roles:
            role = EcspRole(id=data.get('id'), name=data.get('name'))
            role.add(commit=False)

        cls.commit()


class EcspService(Base, BaseMethod):
    __tablename__ = 'ecsp_services'

    SELLER_DIAGNOSE = 'seller diagnose'
    ASIN_DIAGNOSE = 'asin diagnose'
    KW_RANKING_TRACK = 'keywords ranking tracking'
    ASIN_SALE_TRACK = 'asin sale tracking'
    SUPER_URLS = 'super urls'
    KW_SUGGESTION = 'keywords suggestion'
    KW_RANK_IMPROVEMENT = 'keywords ranking improvements'
    KW_RANK_IMPROVEMENT_LV1 = 'keywords ranking improvements (level 1)'
    REVIEW_CLUB = 'review club'
    DYNAMIC_SUPER_URLS = 'dynamic super urls'

    TYPE_MONTHLY = 1
    TYPE_LIFETIME = 2

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(64), nullable=False)
    consumption = Column(BIGINT, default=1)
    service_type = Column(BIGINT, default=1)
    __table_args__ = (Index('ecsp_service_idx', 'name', unique=True),)

    ALL_SERVICES = [
        {'id': 1, 'name': SELLER_DIAGNOSE, 'service_type': TYPE_MONTHLY},
        {'id': 2, 'name': ASIN_DIAGNOSE, 'service_type': TYPE_MONTHLY},
        {'id': 3, 'name': KW_RANKING_TRACK, 'service_type': TYPE_LIFETIME},
        {'id': 4, 'name': ASIN_SALE_TRACK, 'service_type': TYPE_LIFETIME},
        {'id': 5, 'name': SUPER_URLS, 'service_type': TYPE_MONTHLY},
        {'id': 6, 'name': KW_SUGGESTION, 'service_type': TYPE_MONTHLY},
        {'id': 7, 'name': KW_RANK_IMPROVEMENT, 'service_type': TYPE_LIFETIME},
        {'id': 8, 'name': KW_RANK_IMPROVEMENT_LV1, 'consumption': 3,
         'service_type': TYPE_LIFETIME},
        {'id': 9, 'name': REVIEW_CLUB, 'service_type': TYPE_LIFETIME},
        {'id': 10, 'name': DYNAMIC_SUPER_URLS, 'service_type': TYPE_LIFETIME},
    ]

    @classmethod
    def get_by_name(cls, name):
        return DBsession.query(cls).filter(cls.name == name).first()

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return
        for data in cls.ALL_SERVICES:
            role = EcspService(id=data.get('id'), name=data.get('name'),
                               consumption=data.get('consumption', 1),
                               service_type=data.get('service_type'))
            role.add(commit=False)

        cls.commit()

    @classmethod
    def get_lifetime_service(cls):
        return [x['id'] for x in cls.ALL_SERVICES
                if x['service_type'] == cls.TYPE_LIFETIME]

    @classmethod
    def get_monthly_service(cls):
        return [x['id'] for x in cls.ALL_SERVICES
                if x['service_type'] == cls.TYPE_MONTHLY]


class EcspRoleDefaultQuota(Base, BaseMethod):
    __tablename__ = 'ecsp_role_default_quotas'

    id = Column(BIGINT, primary_key=True)
    role_id = Column(BIGINT, ForeignKey('ecsp_roles.id'))
    service_id = Column(BIGINT, ForeignKey('ecsp_services.id'))
    quota = Column(BIGINT, default=0)
    __table_args__ = (Index('ecsp_role_default_quotas_idx', 'role_id',
                            'service_id', unique=True),)

    @classmethod
    def default_data(cls):
        cnt = DBsession.query(cls).count()
        if cnt > 0:
            return

        all_quotas = [
            {'role_id': 1, 'service_id': 1, 'quota': 10},
            {'role_id': 1, 'service_id': 2, 'quota': 50},
            {'role_id': 1, 'service_id': 3, 'quota': 150},
            {'role_id': 1, 'service_id': 4, 'quota': 50},
            {'role_id': 1, 'service_id': 5, 'quota': 150},
            {'role_id': 1, 'service_id': 6, 'quota': 100},
            {'role_id': 1, 'service_id': 7, 'quota': 0},
            {'role_id': 1, 'service_id': 8, 'quota': 0},
            {'role_id': 1, 'service_id': 9, 'quota': 0},
            {'role_id': 1, 'service_id': 10, 'quota': 0},
            {'role_id': 2, 'service_id': 1, 'quota': 100},
            {'role_id': 2, 'service_id': 2, 'quota': 500},
            {'role_id': 2, 'service_id': 3, 'quota': 1500},
            {'role_id': 2, 'service_id': 4, 'quota': 500},
            {'role_id': 2, 'service_id': 5, 'quota': 1500},
            {'role_id': 2, 'service_id': 6, 'quota': 1000},
            {'role_id': 2, 'service_id': 7, 'quota': 5},
            {'role_id': 2, 'service_id': 8, 'quota': 0},
            {'role_id': 2, 'service_id': 9, 'quota': 10},
            {'role_id': 2, 'service_id': 10, 'quota': 1},
        ]
        for data in all_quotas:
            def_quota = EcspRoleDefaultQuota(role_id=data.get('role_id'),
                                             service_id=data.get('service_id'),
                                             quota=data.get('quota'))
            def_quota.add(commit=False)

        cls.commit()

    @classmethod
    def query_by_role_id(cls, role_id):
        return DBsession.query(cls).filter(cls.role_id == role_id).all()


class EcspUserRole(Base, BaseMethod):
    __tablename__ = 'ecsp_user_roles'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    # role_id = Column(BIGINT, ForeignKey('ecsp_roles.id'))
    role_id = Column(BIGINT, nullable=False)
    __table_args__ = (Index('ecsp_user_roles_idx', 'user_id', 'role_id',
                            unique=True),)

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).first()


class EcspUserServiceQuota(Base, BaseMethod):
    '''
    A user's actual quota be calculated as:
    - By default each user holds a role, so the EcspRoleDefaultQuota is used
    - if the user has EcspUserQuota, the row will overwrite the specified
    service's quota
    '''
    __tablename__ = 'ecsp_user_service_quotas'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    service_id = Column(BIGINT, ForeignKey('ecsp_services.id'))
    quota = Column(BIGINT, default=0)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    __table_args__ = (Index('ecsp_user_service_quotas_idx', 'user_id',
                            'service_id', unique=True),)

    @classmethod
    def query_by_user(cls, user_id):
        return DBsession.query(cls).\
            filter(cls.user_id == user_id).all()

    @classmethod
    def get_by_user_service(cls, user_id, service_name):
        service = EcspService.get_by_name(service_name)
        if not service:
            return None
        return DBsession.query(cls).\
            filter(cls.user_id == user_id,
                   cls.service_id == service.id).first()

    @classmethod
    def get_by_user_service_id(cls, user_id, service_id):
        return DBsession.query(cls).\
            filter(cls.user_id == user_id,
                   cls.service_id == service_id).first()

    @classmethod
    def grant_user(cls, user_id, service_id, quota, commit=True):
        if quota <= 0:
            return False

        quota_obj = cls.get_by_user_service_id(user_id, service_id)
        if quota_obj:
            quota_obj = quota
            quota_obj.update(commit)
        else:
            quota_obj = EcspUserServiceQuota(user_id=user_id,
                                             service_id=service_id,
                                             quota=quota)
            quota_obj.add(commit)

        return True

    @classmethod
    def revoke_user(cls, user_id, service_name, commit=True):
        quota_obj = cls.get_by_user_service(user_id, service_name)
        if not quota_obj:
            return True

        quota_obj.quota = 0
        quota_obj.update(commit)

        return True

    @classmethod
    def get_user_service_quota(cls, user_id, service_name):
        service = EcspService.get_by_name(service_name)
        if not service:
            return 0

        service_quota = DBsession.query(cls).\
            filter(cls.user_id == user_id,
                   cls.service_id == service.id).first()
        if service_quota:
            return service_quota.quota

        role = EcspUserRole.get_by_user_id(user_id)
        if not role:
            return service_quota.quota

        role_quota = DBsession.query(EcspRoleDefaultQuota).\
            filter(EcspRoleDefaultQuota.role_id == role.role_id,
                   EcspRoleDefaultQuota.service_id == service.id).first()
        return 0 if not role_quota else role_quota.quota

    @classmethod
    def query_user_all_quotas(cls, user_id):
        results = {}

        role = EcspUserRole.get_by_user_id(user_id)
        if role:
            rows = DBsession.query(EcspRoleDefaultQuota).\
                filter(EcspRoleDefaultQuota.role_id == role.role_id).all()
            if rows:
                results = {row.service_id: row.quota for row in rows}

        rows = DBsession.query(cls).\
            filter(cls.user_id == user_id).all()
        if not rows:
            return results

        for row in rows:
            results[row.service_id] = row.quota
        return results


class EcspUserServiceUsageLog(Base, BaseMethod):
    '''
    The user's service usage log
    '''
    __tablename__ = 'ecsp_user_service_usage_logs'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    service_id = Column(BIGINT, nullable=False)
    month_period = Column(BIGINT, nullable=False)
    usage = Column(BIGINT, nullable=False)
    comments = Column(VARCHAR(512), default='')
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    _SQL_QUERY_USER_SERVICE_USAGE = '''
        WITH service_usages AS (
        select to_char(created_at, 'YYYYMMDD'), sum(usage) as total
        from ecsp_user_service_usage_logs
        where user_id={uid} and service_id={sid}
        and created_at > current_date - interval '7 day'
        group by to_char(created_at, 'YYYYMMDD')
        order by to_char(created_at, 'YYYYMMDD') desc
        limit 7
        )
    SELECT round(AVG(total), 0) FROM service_usages;
    '''

    @classmethod
    def query_user_usages(cls, user_id, month_period=None):
        if not month_period:
            month_period = make_month_period()

        return DBsession.query(cls).\
            filter(cls.user_id == user_id,
                   cls.month_period == month_period).all()

    @classmethod
    def query_user_service_usages(cls, user_id, service_id, month_period=None):
        if not month_period:
            month_period = make_month_period()

        return DBsession.query(cls).\
            filter(cls.user_id == user_id, cls.service_id == service_id,
                   cls.month_period == month_period).all()

    @classmethod
    def query_user_avg_last_7_days_usage(cls, user_id, service_id):
        sql = cls._SQL_QUERY_USER_SERVICE_USAGE.format(**{'uid': user_id,
                                                          'sid': service_id})
        result_proxy = DBsession.execute(sql)
        result = result_proxy.fetchone()
        result_proxy.close()
        return 0 if not result[0] else result[0]


class EcspUserServiceMonthlyQuota(Base, BaseMethod):
    '''
    A user's actual monthly quota

    '''
    __tablename__ = 'ecsp_user_service_monthly_quotas'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    month_period = Column(BIGINT, default=make_month_period)
    service_id = Column(BIGINT, ForeignKey('ecsp_services.id'))
    quota = Column(BIGINT, default=0)

    __table_args__ = (Index('ecsp_user_service_monthly_quotas_idx', 'user_id',
                            'month_period', 'service_id', unique=True),)

    @classmethod
    def query_user_all_quotas(cls, user_id, month_period=None):
        if not month_period:
            month_period = make_month_period()

        rows = DBsession.query(cls).\
            filter(cls.user_id == user_id,
                   cls.month_period == month_period).all()
        return {row.service_id: row.quota for row in rows}

    @classmethod
    def get_by_user_service(cls, user_id, service_name, month_period=None):
        service = EcspService.get_by_name(service_name)
        if not service:
            return None

        return cls.get_by_user_service_id(user_id, service.id, month_period)

    @classmethod
    def get_by_user_service_id(cls, user_id, service_id, month_period=None):
        if not month_period:
            month_period = make_month_period()

        return DBsession.query(cls).\
            filter(cls.user_id == user_id, cls.month_period == month_period,
                   cls.service_id == service_id).first()

    @classmethod
    def has_more_service_quota(cls, user_id, service_name, expected_usage=1):
        if expected_usage < 0:
            return False

        quota_obj = cls.get_by_user_service(user_id, service_name)
        return False if not quota_obj else quota_obj.quota >= expected_usage

    @classmethod
    def grant_user(cls, user_id, service_name, value):
        if value <= 0:
            return False

        quota_obj = cls.get_by_user_service(user_id, service_name)
        if quota_obj:
            quota_obj.quota = value
            return quota_obj.update()

        service = EcspService.get_by_name(service_name)
        if not service:
            return False

        month_period = make_month_period()
        EcspUserServiceQuota.grant_user(user_id=user_id,
                                        service_id=service.id,
                                        quota=value, commit=False)
        quota_obj = EcspUserServiceMonthlyQuota(user_id=user_id,
                                                month_period=month_period,
                                                service_id=service.id,
                                                quota=value)
        quota_obj.add(False)

        usage = EcspUserServiceUsageLog(user_id=user_id,
                                        service_id=service.id,
                                        month_period=month_period,
                                        usage=value * -1,
                                        comments='grant service')
        usage.add(False)

        return BaseMethod.commit()

    @classmethod
    def revoke_user(cls, user_id, service_name):
        quota_obj = cls.get_by_user_service(user_id, service_name)
        if not quota_obj or quota_obj.quota <= 0:
            return
        quota_obj.consume(quota_obj.quota, comments='revoke service')

    def has_more_quota(self, user_id, expected_usage=1):
        if expected_usage < 0:
            return False
        return self.quota >= expected_usage

    def produce(self, value, comments=''):
        if value <= 0:
            return False
        self.quota += value
        self.update(False)
        usage = EcspUserServiceUsageLog(user_id=self.user_id,
                                        service_id=self.service_id,
                                        month_period=self.month_period,
                                        usage=value * -1,
                                        comments='add quota: %s' % comments)
        usage.add(False)
        return self.commit()

    def consume(self, value=0, comments='', commit=True):
        if value < 0:
            return False

        if value == 0:
            service = EcspService.get_by_id(self.service_id)
            if not service:
                return False
            value = service.consumption

        if self.quota < value:
            return False

        self.quota -= value
        self.update(False)
        usage = EcspUserServiceUsageLog(user_id=self.user_id,
                                        service_id=self.service_id,
                                        month_period=self.month_period,
                                        usage=value,
                                        comments=comments)
        usage.add(False)

        if commit:
            self.commit()

        return True


class EcspSuperUrlGroup(Base, BaseMethod):
    __tablename__ = 'ecsp_super_url_groups'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    market_place_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    merchant_id = Column(VARCHAR(64), nullable=False)
    keywords = Column(VARCHAR(512), nullable=False)
    associate_tag = Column(VARCHAR(64), nullable=False)
    description = Column(VARCHAR(512), nullable=False)
    url = Column(VARCHAR(1024), nullable=False)
    is_dynamic = Column(BOOLEAN, nullable=False)
    name = Column(VARCHAR(64), nullable=False)


class EcspSuperUrl(Base, BaseMethod):
    __tablename__ = 'ecsp_super_urls'

    id = Column(BIGINT, primary_key=True)
    group_id = Column(BIGINT, ForeignKey('ecsp_super_url_groups.id'))
    name = Column(VARCHAR(128), nullable=False)
    url = Column(VARCHAR(1024))
    key = Column(VARCHAR(128))
    salt = Column(VARCHAR(128))
    v1 = Column(VARCHAR(255))
    v2 = Column(VARCHAR(255))
    v3 = Column(VARCHAR(255))
    v4 = Column(VARCHAR(255))
    v5 = Column(VARCHAR(255))
    v6 = Column(VARCHAR(255))
    v7 = Column(VARCHAR(255))
    v8 = Column(VARCHAR(255))
    v9 = Column(VARCHAR(255))
    v10 = Column(VARCHAR(255))

    @classmethod
    def get_by_prj_id(cls, prj_id):
        return DBsession.query(cls).filter(cls.v10 == str(prj_id)).first()


class EcspClick(Base, BaseMethod):
    '''
    The superurl clicks table
    In current phase, there will be not so many clicks, so just put it in
    normal databas instead of data warehouse
    '''
    __tablename__ = 'ecsp_clicks'

    click_id = Column(VARCHAR(255), primary_key=True)
    group_id = Column(BIGINT, nullable=False)
    url_id = Column(BIGINT, nullable=False)
    ip = Column(VARCHAR(255))
    referer = Column(VARCHAR(255))
    v1 = Column(VARCHAR(255))
    v2 = Column(VARCHAR(255))
    v3 = Column(VARCHAR(255))
    v4 = Column(VARCHAR(255))
    v5 = Column(VARCHAR(255))
    v6 = Column(VARCHAR(255))
    v7 = Column(VARCHAR(255))
    v8 = Column(VARCHAR(255))
    v9 = Column(VARCHAR(255))
    v10 = Column(VARCHAR(255))
    country = Column(VARCHAR(255))
    isp = Column(VARCHAR(255))
    user_agent = Column(VARCHAR(255))
    os_version = Column(VARCHAR(255))
    device_detail = Column(VARCHAR(255))
    ua_detail = Column(VARCHAR(255))
    browser = Column(VARCHAR(255))
    device_type = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP(timezone=True))

    @staticmethod
    def do_vacuum():
        result = DBsession_autocommit.execute('VACUUM ecsp_clicks;')
        result.close()


class EcspArchiveTable(Base, BaseMethod):
    __tablename__ = 'ecsp_archive_tables'
    __CREATE_ARCHIVE_TABLE_SQL = '''
        CREATE TABLE {archive_table} AS SELECT * FROM ecsp_clicks WHERE 1=2;
    '''

    id = Column(BIGINT, primary_key=True)
    table_name = Column(VARCHAR(255))
    CreatedAt = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    @classmethod
    def get_latest(cls):
        return DBsession.query(cls).order_by(cls.id.desc()).first()

    def add(self, commit=True):
        DBsession.add(self)
        BaseMethod.execute(self.__CREATE_ARCHIVE_TABLE_SQL
                           .format(**{'archive_table': self.table_name}))
        if commit:
            BaseMethod.commit()


class AmzSellerChannel(Base, BaseMethod):
    __tablename__ = 'amz_seller_channels'

    id = Column(BIGINT, primary_key=True)
    free = Column(BOOLEAN, default=False)
    cpc = Column(BOOLEAN, default=False)
    social_media = Column(BOOLEAN, default=False)
    super_url = Column(BOOLEAN, default=False)
    create_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzAdvertisingAPIAccount(Base, BaseMethod):
    __tablename__ = 'amz_advertising_api_accounts'

    id = Column(BIGINT, primary_key=True)
    account_name = Column(VARCHAR(255), nullable=False)
    is_active = Column(Boolean, default=True)
    key = Column(VARCHAR(255), nullable=False)
    secret = Column(VARCHAR(255), nullable=False)
    last_used = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    supported_markets = Column(VARCHAR(255), nullable=False)

    @classmethod
    def query_active_account(cls, market='US'):
        active_account = DBsession.query(cls).filter(
            cls.is_active,
            cls.supported_markets.ilike('%{}%'.format(market))).\
            order_by(cls.last_used).first()
        if not active_account:
            return None, None
        account_key = active_account.key
        account_secret = active_account.secret
        active_account.last_used = datetime.utcnow().\
            replace(tzinfo=pytz.UTC)
        active_account.update()
        return account_key, account_secret


class AmzUserPromotion(Base, BaseMethod):
    __tablename__ = 'amz_user_promotions'
    _STATUS_PAUSED = 1
    _STATUS_STARTED = 2
    _STATUS_ARCHIVED = 3

    _TRANSIT_MAP = {
        _STATUS_PAUSED: [_STATUS_STARTED, _STATUS_ARCHIVED],
        _STATUS_STARTED: [_STATUS_PAUSED],
        _STATUS_ARCHIVED: []}

    _DISCOUNT_TYPE_PERCENTAGE = 1
    _DISCOUNT_TYPE_PRICE = 2

    _COUPON_TYPE_MUTIPLE = 1
    _COUPON_TYPE_SINGLE = 2

    __PRO_COUNT = 120
    __LIMIT = 120

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    merchant_id = Column(VARCHAR(64), nullable=False)
    marketplace_id = Column(BIGINT, nullable=False)
    status = Column(BIGINT, default=_STATUS_PAUSED, nullable=False)
    support_email = Column(VARCHAR(255), nullable=False)
    price = Column(REAL, nullable=False)
    discount_value = Column(REAL, default=0, nullable=False)
    discount_type = Column(BIGINT, default=_DISCOUNT_TYPE_PERCENTAGE)
    final_price = Column(REAL, default=0, nullable=False)
    discount_percentage = Column(REAL, default=0, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow,
                        nullable=True)
    end_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow,
                      nullable=True)
    have_ever_started = Column(Boolean, default=False)
    title = Column(VARCHAR(512), nullable=False)
    description = Column(VARCHAR(65535), nullable=False)
    short_desc = Column(VARCHAR(128), nullable=False)
    is_fba = Column(BOOLEAN, default=True)
    product_group = Column(VARCHAR(64), nullable=False)
    coupon_type = Column(BIGINT, default=_COUPON_TYPE_MUTIPLE)
    associate_tag = Column(VARCHAR(64), default='')
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    __QUERY_SQL = '''
    SELECT * FROM amz_user_promotions
    WHERE end_date > '{now_time}'
    AND status=2
    AND title ILIKE '%{title}%'
    {market}
    {category}
    ORDER BY {order_params}
    OFFSET {offset} LIMIT {limit}
    '''

    @classmethod
    def save(cls, user_id, asin, merchant_id, marketplace_id,
             promotion_detail, commit=True):
        obj = cls.query_by_userid_asin_market(user_id, asin, marketplace_id)
        add = False
        if obj is None:
            add = True
            obj = AmzUserPromotion(user_id=user_id,
                                   marketplace_id=marketplace_id,
                                   asin=asin)

        obj.merchant_id = merchant_id
        obj.support_email = promotion_detail['support_email']
        obj.price = promotion_detail['price']
        obj.discount_value = promotion_detail['discount_value']
        obj.discount_type = promotion_detail['discount_type']
        obj.final_price = promotion_detail['final_price']
        obj.discount_percentage = promotion_detail['discount_percentage']
        obj.start_date = datetime.strptime(promotion_detail['start_date'],
                                           '%Y-%m-%d').replace(tzinfo=pytz.UTC)
        obj.end_date = datetime.strptime(promotion_detail['end_date'],
                                         '%Y-%m-%d').replace(tzinfo=pytz.UTC)
        obj.title = promotion_detail['title']
        obj.description = promotion_detail['description']
        obj.short_desc = promotion_detail['short_desc']
        obj.is_fba = promotion_detail['is_fba']
        obj.product_group = promotion_detail['product_group']
        obj.coupon_type = promotion_detail['coupon_type']
        obj.associate_tag = promotion_detail['associate_tag']

        if add:
            obj.add(commit=False)
        else:
            obj.update(commit=False)

        if commit:
            obj.commit()
        return obj

    @classmethod
    def query_by_user_id_promotion_id(cls, user_id, promotion_id):
        return DBsession.query(cls).\
            filter(cls.user_id == user_id,
                   cls.id == promotion_id).first()

    def archive(self):
        self.status = AmzUserPromotion._STATUS_ARCHIVED
        self.update()

    def pause(self):
        self.status = AmzUserPromotion._STATUS_PAUSED
        self.update()

    def start(self):
        self.status = AmzUserPromotion._STATUS_STARTED
        self.update()

    def check_status(self):
        archived_time = datetime.utcnow() - timedelta(days=7)
        if self.is_paused() and\
                self.end_date <= archived_time.replace(tzinfo=pytz.UTC):
            self.archive()
        elif self.is_started() and \
                self.end_date < datetime.utcnow().replace(tzinfo=pytz.UTC)\
                or not AmzPromotionCoupon.query_unassigned_coupon(
                    self.id):
            self.pause()

    def update_status(self, status):
        valid_status = self._TRANSIT_MAP[self.status]
        if not valid_status or status not in valid_status:
            raise Exception("Invalid status transition from %s to %s" %
                            (self.status, status))

        self.status = status
        self.update()
        self.check_status()

    def is_archived(self):
        return self.status == AmzUserPromotion._STATUS_ARCHIVED

    def is_paused(self):
        return self.status == AmzUserPromotion._STATUS_PAUSED

    def is_started(self):
        return self.status == AmzUserPromotion._STATUS_STARTED

    @classmethod
    def query_by_userid(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def query_by_userid_asin_market(cls, user_id, asin, marketplace_id):
        return DBsession.query(cls).filter(
            cls.user_id == user_id, cls.asin == asin,
            cls.marketplace_id == marketplace_id,
            cls.status != cls._STATUS_ARCHIVED).first()

    @classmethod
    def query_by_params(cls, page, market=0, title='', order_params='end_date',
                        category_list=''):
        now = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(seconds=5)
        category = ''
        if category_list:
            category_list = json.loads(category_list)
            category = 'AND product_group IN (%s)' \
                % ('\'' + '\',\''.join(category_list) + '\'')

        market_statement = ''
        if market:
            market_statement = 'AND marketplace_id=%d' % market

        return fetchall(cls.__QUERY_SQL.
                        format(**{'title': title,
                                  'order_params': order_params,
                                  'market': market_statement,
                                  'category': category,
                                  'now_time': now,
                                  'offset':
                                  (page - 1) * cls.__PRO_COUNT,
                                  'limit': cls.__LIMIT}))

    @classmethod
    def get_by_prom_ids(cls, prom_ids):
        return DBsession.query(cls).filter(cls.id.in_(prom_ids)).all()


class AmzPromotionCoupon(Base, BaseMethod):
    __tablename__ = 'amz_promotion_coupons'

    id = Column(BIGINT, primary_key=True)
    promotion_id = Column(BIGINT, ForeignKey('amz_user_promotions.id'))
    coupon = Column(VARCHAR(64), nullable=False)
    is_assigned = Column(BOOLEAN, default=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    __COUNT_COUPON_SQL = '''
    SELECT promotion_id, count(coupon) FROM amz_promotion_coupons
    WHERE promotion_id IN ({promotion_ids}) AND is_assigned=False
    GROUP BY promotion_id
    '''

    @classmethod
    def query_unassigned_coupon(cls, prom_id):
        return DBsession.query(cls).filter(
            cls.promotion_id == prom_id, cls.is_assigned != true()).all()

    @classmethod
    def query_by_promotion_id_coupon(cls, promotion_id, coupon):
        return DBsession.query(cls).filter(cls.promotion_id == promotion_id,
                                           cls.coupon == coupon).first()

    @classmethod
    def create_or_update_coupons(cls, promotion_id, coupons):
        all_coupons = cls.query_unassigned_coupon(promotion_id)
        for coupon in coupons:
            obj = AmzPromotionCoupon.query_by_promotion_id_coupon(promotion_id,
                                                                  coupon)
            if obj:
                continue

            obj = AmzPromotionCoupon(promotion_id=promotion_id,
                                     coupon=coupon)
            obj.add(commit=False)

        for exist_coupon in all_coupons:
            if exist_coupon.coupon not in coupons:
                exist_coupon.delete(commit=False)
        cls.commit()

    @classmethod
    def query_one_unassigned_coupon(cls, prom_id):
        return DBsession.query(cls).filter(
            cls.promotion_id == prom_id, cls.is_assigned != true()).first()

    def check_assigned(self):
        return self.is_assigned

    def assign(self, commit=False):
        self.is_assigned = True
        self.update(commit=False)

    def unassign(self):
        self.is_assigned = False
        self.update()

    @classmethod
    def query_by_promotion_ids(cls, promotion_ids):
        return fetchall(cls.__COUNT_COUPON_SQL.format(**{
            'promotion_ids': ','.join(promotion_ids)}))

    @classmethod
    def get_by_coupon_ids(cls, coupon_ids):
        return DBsession.query(cls).filter(cls.id.in_(coupon_ids)).all()


class AmzReviewerRequestCoupon(Base, BaseMethod):
    __tablename__ = 'amz_reviewer_request_coupons'

    _STATUS_PENDING = 1
    _STATUS_APPROVED = 2
    _STATUS_DISAPPROVED = 3
    _STATUS_EXPIRED = 4
    _STATUS_ACCEPTED = 5
    _STATUS_REVIEWED = 6
    _STATUS_CHECK_CONFIRM = 10
    _STATUS_CONFIRM_REVIEWED = 7
    _STATUS_DECLINED = 8
    _STATUS_DELETED = 9

    _SQL_QUERY_REVIEW_INFO = '''select rrc.user_id, r.rank_number,
    r.total_reviews,
    r.helpful_votes, re.accepted_reviews, re.confirmed_reviews,
    re.last_reviewed as last_reviewed, r.reviewer_id, s.score as score
    from amz_reviewer_request_coupons as rrc inner join ecsp_reviewers as re
    on rrc.user_id=re.user_id
    inner join amz_reviewers as r on re.amz_reviewer_{marketplace}_id=r.id
    inner join ecsp_reviewer_scores as s on s.user_id=rrc.user_id
    where rrc.promotion_id = {prom_id}
    and rrc.status={status}'''

    _SCORE_MAP = {'decline': -2, 'confirm_review': 5,
                  'not_confirm_review': -5, 'with_words': 1, 'with_photos': 2,
                  'with_videos': 3, 'expire_review': -5, 'expire_accept': -2}
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    status = Column(BIGINT, default=_STATUS_PENDING)
    promotion_id = Column(BIGINT, ForeignKey('amz_user_promotions.id'))
    coupon_id = Column(BIGINT, ForeignKey('amz_promotion_coupons.id'),
                       nullable=True)
    requested_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    approved_at = Column(TIMESTAMP(timezone=True))
    accepted_at = Column(TIMESTAMP(timezone=True))
    reviewed_at = Column(TIMESTAMP(timezone=True))
    confirm_reviewed_at = Column(TIMESTAMP(timezone=True))
    declined_at = Column(TIMESTAMP(timezone=True))

    @classmethod
    def query_expire_accept_coupon(cls):
        expire_time = datetime.utcnow().replace(tzinfo=pytz.UTC) -\
            timedelta(days=3)
        return DBsession.query(cls).filter(cls.status == cls._STATUS_APPROVED,
                                           cls.approved_at < expire_time).all()

    @classmethod
    def query_expire_review_coupon(cls):
        expire_time = datetime.utcnow().replace(tzinfo=pytz.UTC) -\
            timedelta(days=15)
        return DBsession.query(cls).filter(cls.status == cls._STATUS_ACCEPTED,
                                           cls.accepted_at < expire_time).all()

    @classmethod
    def request_for_coupon(cls, reviewer_id, promotion_id, seller_id):
        promotion = AmzUserPromotion.\
            query_by_user_id_promotion_id(seller_id, promotion_id)
        if not promotion:
            return -1

        reviewer_request = DBsession.query(cls).\
            filter(cls.promotion_id == promotion_id,
                   cls.user_id == reviewer_id).all()
        if reviewer_request:
            return -1

        new_request = AmzReviewerRequestCoupon(user_id=reviewer_id,
                                               status=cls._STATUS_PENDING,
                                               promotion_id=promotion_id)
        return new_request.id if new_request.add() else -1

    @classmethod
    def query_pending_request(cls, prom_id, website, marketplace):
        sql = cls._SQL_QUERY_REVIEW_INFO.\
            format(**{'prom_id': prom_id, 'status': cls._STATUS_PENDING,
                      'marketplace': marketplace})
        request = fetchall(sql)
        result = []
        url = "http://%s/gp/pdp/profile/%s/ref=cm_cr_dp_pdp"
        for x in request:
            last_reviewed = x.last_reviewed.strftime('%Y-%m-%d')\
                if x.last_reviewed else '--'
            result.append(dict(reviewer_rank=x.rank_number,
                               request_id=x.user_id,
                               total_reviews=x.total_reviews,
                               helpful_votes=x.helpful_votes,
                               accepted_reviews=x.accepted_reviews,
                               confirmed_reviews=x.confirmed_reviews,
                               last_reviewed=last_reviewed,
                               request_status=1,
                               url=url % (website, x.reviewer_id),
                               reviewer_score=x.score))
        return result

    @classmethod
    def query_reviewer_request_by_status(cls, reviewer_id, promotion_id,
                                         status):
        return DBsession.query(cls).\
            filter(cls.user_id == reviewer_id,
                   cls.promotion_id == promotion_id,
                   cls.status == status).first()

    @classmethod
    def check_promotion_and_request(cls, promotion_id, reviewer_id, seller_id,
                                    status):
        promotion = AmzUserPromotion.\
            query_by_user_id_promotion_id(seller_id, promotion_id)
        if not promotion:
            return False, None

        coupon_request = cls.\
            query_reviewer_request_by_status(reviewer_id, promotion_id,
                                             status)
        if coupon_request:
            return True, coupon_request
        else:
            return False, None

    @classmethod
    def disapprove_coupon_request(cls, promotion_id, reviewer_id, seller_id):
        result, req = cls.check_promotion_and_request(promotion_id,
                                                      reviewer_id,
                                                      seller_id,
                                                      cls._STATUS_PENDING)
        return req.disapprove() if result else False

    @classmethod
    def approve_coupon_request(cls, promotion_id, reviewer_id, seller_id):
        result, req = cls.check_promotion_and_request(promotion_id,
                                                      reviewer_id,
                                                      seller_id,
                                                      cls._STATUS_PENDING)
        return req.approve() if result else False

    @classmethod
    def query_visible_request_by_user_id(cls, reviewer_id):
        invisible = [cls._STATUS_DECLINED, cls._STATUS_DELETED,
                     cls._STATUS_REVIEWED, cls._STATUS_CHECK_CONFIRM,
                     cls._STATUS_CONFIRM_REVIEWED]
        return DBsession.query(cls).filter(cls.user_id == reviewer_id,
                                           ~cls.status.in_(invisible)).all()

    @classmethod
    def accept_request(cls, seller_id, promotion_id, reviewer_id):
        result, req = cls.check_promotion_and_request(promotion_id,
                                                      reviewer_id,
                                                      seller_id,
                                                      cls._STATUS_APPROVED)
        return req.accept(commit=True) if result else False

    @classmethod
    def decline_request(cls, seller_id, promotion_id, reviewer_id):
        result, req = cls.check_promotion_and_request(promotion_id,
                                                      reviewer_id,
                                                      seller_id,
                                                      cls._STATUS_APPROVED)
        state = req.decline(commit=True) if result else False
        if not state:
            return False
        reviewer = EcspReviewerScore.get_by_user_id(req.user_id)
        reviewer.score += reviewer.lasting_bad_reviews *\
            cls._SCORE_MAP['decline']
        reviewer.upgrade_demote_role(commit=False)
        return reviewer.update()

    @classmethod
    def reviewer_review(cls, seller_id, promotion_id, reviewer_id):
        result, req = cls.check_promotion_and_request(promotion_id,
                                                      reviewer_id,
                                                      seller_id,
                                                      cls._STATUS_ACCEPTED)
        return req.review(commit=True) if result else False

    @classmethod
    def reset_reviewer_review(cls, coupon_request_id):
        coupon_request = AmzReviewerRequestCoupon.\
            get_by_id(coupon_request_id)
        if not coupon_request:
            return False
        state = coupon_request.reset_reviewed()
        if not state:
            return False
        reviewer = EcspReviewerScore.get_by_user_id(coupon_request.user_id)
        reviewer.score += reviewer.lasting_bad_reviews *\
            cls._SCORE_MAP['not_confirm_review']
        reviewer.upgrade_demote_role(commit=False)
        return reviewer.update()

    @classmethod
    def delete_request(cls, seller_id, promotion_id, reviewer_id,
                       coupon_request_id):
        promotion = AmzUserPromotion.\
            query_by_user_id_promotion_id(seller_id, promotion_id)
        coupon_request = cls.get_by_id(coupon_request_id)
        if not promotion or not coupon_request or\
                promotion_id != coupon_request.promotion_id:
            return False

        if coupon_request.status == cls._STATUS_PENDING:
            return coupon_request.delete()
        else:
            return coupon_request.soft_delete(commit=True)

    @classmethod
    def check_request_review(cls):
        result = []
        deadline = datetime.utcnow().\
            replace(tzinfo=pytz.UTC) - timedelta(days=1)

        all_reviewed_request = DBsession.query(cls).\
            filter(cls.status == cls._STATUS_REVIEWED,
                   cls.reviewed_at > deadline).all()
        for reviewed_request in all_reviewed_request:
            ecsp_reviewer = EcspReviewer.\
                query_by_user_id(reviewed_request.user_id)
            prom = AmzUserPromotion.get_by_id(reviewed_request.promotion_id)
            if ecsp_reviewer and prom:
                amz_reviewer = AmzReviewer.\
                    get_by_id(ecsp_reviewer.get_amz_reviewer_id(
                              ecsp_reviewer.origin_marketplace_id))
                result.append([amz_reviewer.reviewer_id,
                               prom.asin,
                               prom.marketplace_id,
                               reviewed_request.id,
                               prom.user_id])
        return result

    @classmethod
    def confirm_request(cls, coupon_request_id, review_data):
        coupon_request = AmzReviewerRequestCoupon.\
            get_by_id(coupon_request_id)
        if not coupon_request:
            return False
        status = coupon_request.confirm(commit=True)
        if not status:
            return False
        reviewer = EcspReviewerScore.get_by_user_id(coupon_request.user_id)
        reviewer.score += cls._SCORE_MAP['confirm_review']
        for item in review_data.keys():
            reviewer.score += cls._SCORE_MAP[item]
        reviewer.upgrade_demote_role(commit=False)
        return reviewer.update()

    @classmethod
    def query_requested_coupon_by_reviewer_id(cls, reviewer_id):
        return DBsession.query(cls).filter(cls.user_id == reviewer_id).all()

    @classmethod
    def expire_review(cls, request_id):
        coupon_request = AmzReviewerRequestCoupon.\
            get_by_id(request_id)
        if not coupon_request:
            return False
        state = coupon_request.decline(commit=True)
        if not state:
            return False
        reviewer = EcspReviewerScore.get_by_user_id(coupon_request.user_id)
        reviewer.score += reviewer.lasting_bad_reviews * \
            cls._SCORE_MAP['expire_review']
        reviewer.upgrade_demote_role(commit=False)
        return reviewer.update()

    @classmethod
    def expire_accept(cls, request_id):
        coupon_request = AmzReviewerRequestCoupon.\
            get_by_id(request_id)
        if not coupon_request:
            return False
        state = coupon_request.decline(commit=True)
        if not state:
            return False
        reviewer = EcspReviewerScore.get_by_user_id(coupon_request.user_id)
        reviewer.score += reviewer.lasting_bad_reviews * \
            cls._SCORE_MAP['expire_accept']
        reviewer.upgrade_demote_role(commit=False)

        return reviewer.update()

    def disapprove(self):
        self.status = AmzReviewerRequestCoupon._STATUS_DISAPPROVED
        return self.update()

    def approve(self):
        coupon = AmzPromotionCoupon.\
            query_one_unassigned_coupon(self.promotion_id)
        if not coupon or coupon.check_assigned():
            return False
        self.coupon_id = coupon.id
        self.status = AmzReviewerRequestCoupon._STATUS_APPROVED
        self.approved_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        try:
            coupon.assign(commit=False)
            self.update(commit=False)
            return self.commit()
        except:
            return False

    def query_coupon(self, status, coupon_id):
        visible = [AmzReviewerRequestCoupon._STATUS_ACCEPTED,
                   AmzReviewerRequestCoupon._STATUS_REVIEWED,
                   AmzReviewerRequestCoupon._STATUS_CHECK_CONFIRM,
                   AmzReviewerRequestCoupon._STATUS_CONFIRM_REVIEWED]
        if status not in visible:
            return ''
        coupon = AmzPromotionCoupon.get_by_id(coupon_id)
        return coupon.coupon if coupon else ''

    def accept(self, commit=False):
        reviewer = EcspReviewer.query_by_user_id(self.user_id)
        if not reviewer:
            return False
        self.status = AmzReviewerRequestCoupon._STATUS_ACCEPTED
        self.accepted_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        reviewer.add_accepted_reviews(commit=False)
        return self.update(commit=commit)

    def decline(self, commit=False):
        coupon = AmzPromotionCoupon.get_by_id(self.coupon_id)
        if not coupon:
            return False
        try:
            coupon.is_assigned = False
            coupon.update(commit=False)
            self.status = AmzReviewerRequestCoupon._STATUS_DECLINED
            self.coupon_id = None
            self.declined_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
            self.update(commit=False)
            return self.commit() if commit else True
        except:
            return False

    def review(self, commit=False):
        reviewer = EcspReviewer.query_by_user_id(self.user_id)
        if not reviewer:
            return False
        self.status = AmzReviewerRequestCoupon._STATUS_REVIEWED
        self.reviewed_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        reviewer.save_last_reviewed(commit=False)
        return self.update(commit=commit)

    def check(self, commit=False):
        self.status = AmzReviewerRequestCoupon._STATUS_CHECK_CONFIRM
        return self.update(commit=commit)

    def confirm(self, commit=False):
        reviewer = EcspReviewer.query_by_user_id(self.user_id)
        if not reviewer:
            return False
        self.status = AmzReviewerRequestCoupon._STATUS_CONFIRM_REVIEWED
        self.confirm_reviewed_at = datetime.utcnow().replace(tzinfo=pytz.UTC)
        reviewer.add_confirmed_reviews(commit=False)
        return self.update(commit=commit)

    def soft_delete(self, commit=False):
        self.status = AmzReviewerRequestCoupon._STATUS_DELETED
        self.coupon_id = None
        return self.update(commit=commit)

    def reset_reviewed(self):
        self.status = AmzReviewerRequestCoupon._STATUS_REVIEWED
        return self.update()


class AmzReviewer(Base, BaseMethod):
    __tablename__ = 'amz_reviewers'
    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, nullable=False)
    rank_number = Column(BIGINT, default=0)
    name = Column(VARCHAR(512))
    reviewer_id = Column(VARCHAR(64))
    image = Column(VARCHAR(512))
    email = Column(VARCHAR(512))
    link = Column(VARCHAR(512))
    total_reviews = Column(BIGINT, default=0)
    helpful_votes = Column(BIGINT, default=0)
    percent_helpful = Column(BIGINT, default=0)
    medal = Column(JSONB)
    review_stat = Column(JSONB)
    create_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    @classmethod
    def get_reviewer_has_email(cls):
        return DBsession.query(cls).filter(cls.email.like('%@%')).all()

    @classmethod
    def get_by_reviewer_id_market(cls, reviewer_id, market):
        return DBsession.query(cls).\
            filter(cls.reviewer_id == reviewer_id,
                   cls.marketplace_id == market).first()

    @classmethod
    def get_by_rank_number_market(cls, rank, market):
        return DBsession.query(cls).\
            filter(cls.rank_number == rank,
                   cls.marketplace_id == market).first()

    @classmethod
    def save(cls, market, rank, name, reviewer_id, image, email, link,
             total_reviews, helpful_votes, percent_helpful, medal,
             commit=True):
        obj = cls.get_by_reviewer_id_market(reviewer_id, market)
        if obj:
            obj.rank_number = rank
            obj.name = name
            obj.image = image
            obj.email = email
            obj.link = link
            obj.total_reviews = total_reviews if total_reviews != 0 else\
                obj.total_reviews
            obj.helpful_votes = helpful_votes
            obj.percent_helpful = percent_helpful if percent_helpful != 0 else\
                obj.percent_helpful
            obj.medal = medal
            obj.update(commit=False)
        else:
            obj = AmzReviewer(market, rank, name, reviewer_id, image,
                              email, link, total_reviews, helpful_votes,
                              percent_helpful, medal)
            obj.add(commit=False)

        if commit:
            obj.commit()

    @classmethod
    def get_by_marketplace_id(cls, market):
        return DBsession.query(cls).filter(cls.marketplace_id == market).all()

    def update_review_stat(self, commit=True):
        month_reviews = AmzReviewerInfo.get_month_reviews(self.marketplace_id,
                                                          self.reviewer_id)
        if len(month_reviews) == 0:
            return
        data = {k: v for k, v in self.review_stat.items()}
        # update month_reviews
        data['month_reviews'] = len(month_reviews)

        # update average words
        words_count = 0
        re_words = re.compile('(\w+)')
        for review in month_reviews:
            words_count += len(re_words.findall(review.review_text))
        data['average_words'] = words_count / len(month_reviews)
        self.review_stat = data
        self.update(commit=commit)


class AmzReviewerInfo(Base, BaseMethod):
    __tablename__ = 'amz_reviewer_infos'
    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, nullable=False)
    reviewer_id = Column(VARCHAR(64), nullable=False)
    asin = Column(VARCHAR(16), nullable=False)
    rate = Column(BIGINT)
    review_title = Column(VARCHAR(512))
    review_text = Column(VARCHAR(65535))
    review_date = Column(TIMESTAMP(timezone=True))
    image = Column(JSONB)
    media = Column(JSONB)
    create_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    _DISTINCT_REVIEWER_ID = '''
    SELECT distinct(reviewer_id), marketplace_id FROM amz_reviewer_infos
    '''

    @classmethod
    def get_by_reviewer_id_market(cls, reviewer_id, market):
        return DBsession.query(cls).\
            filter(cls.reviewer_id == reviewer_id,
                   cls.marketplace_id == market).all()

    @classmethod
    def order_by_review_date(cls, reviewer_id, market):
        return DBsession.query(cls).\
            filter(cls.reviewer_id == reviewer_id,
                   cls.marketplace_id == market).\
            order_by(cls.review_date.desc()).first()

    @classmethod
    def get_review_by_reviewer_id_asin(cls, market, reviewer_id, asin):
        return DBsession.query(cls).\
            filter(cls.marketplace_id == market,
                   cls.reviewer_id == reviewer_id, cls.asin == asin).\
            order_by(cls.review_date.desc()).first()

    @classmethod
    def get_distinct_reviewer_id_market(cls):
        return fetchall(cls._DISTINCT_REVIEWER_ID)

    @classmethod
    def get_month_reviews(cls, market, reviewer_id):
        month_ago = datetime.today() - timedelta(days=30)
        return DBsession.query(cls).filter(
            cls.marketplace_id == market, cls.review_date >= month_ago,
            cls.reviewer_id == reviewer_id).all()


class EcspReviewer(Base, BaseMethod):
    __tablename__ = 'ecsp_reviewers'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    origin_marketplace_id = Column(BIGINT)
    amz_reviewer_us_id = Column(BIGINT, default=0)
    amz_reviewer_uk_id = Column(BIGINT, default=0)
    amz_reviewer_de_id = Column(BIGINT, default=0)
    amz_reviewer_fr_id = Column(BIGINT, default=0)
    amz_reviewer_ca_id = Column(BIGINT, default=0)
    amz_reviewer_es_id = Column(BIGINT, default=0)
    amz_reviewer_it_id = Column(BIGINT, default=0)
    accepted_reviews = Column(BIGINT, default=0)
    confirmed_reviews = Column(BIGINT, default=0)
    allow_send_email = Column(BOOLEAN, default=True)
    ref = Column(VARCHAR(64))
    last_reviewed = Column(TIMESTAMP(timezone=True), nullable=True)

    market_attr_map = {1: 'amz_reviewer_us_id', 3: 'amz_reviewer_uk_id',
                       4: 'amz_reviewer_de_id', 5: 'amz_reviewer_fr_id',
                       7: 'amz_reviewer_ca_id', 44551: 'amz_reviewer_es_id',
                       35691: 'amz_reviewer_it_id'}

    @classmethod
    def query_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).first()

    def save_last_reviewed(self, commit=False):
        self.last_reviewed = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.update(commit=commit)

    def add_confirmed_reviews(self, commit=True):
        self.confirmed_reviews += 1
        self.update(commit=commit)

    def add_accepted_reviews(self, commit=True):
        self.accepted_reviews += 1
        self.update(commit=commit)

    def set_amz_reviewer_id(self, market, amz_reviewer_id):
        setattr(self, self.market_attr_map[market], amz_reviewer_id)
        self.update()

    def get_amz_reviewer_id(self, marketplace):
        return getattr(self, self.market_attr_map[marketplace])


class EcspRefTag(Base, BaseMethod):
    __tablename__ = 'ecsp_ref_tags'

    id = Column(BIGINT, primary_key=True)
    ref = Column(VARCHAR(64))
    marketplace_id = Column(BIGINT)
    tag = Column(VARCHAR(64))

    @classmethod
    def get_tag_by_ref(cls, ref):
        return DBsession.query(cls).filter(cls.ref == ref).all()

    @classmethod
    def default_data(cls):
        all_data = [
            {'ref': 'xiao', 'marketplace_id': 1, 'tag': 'xiao_us'},
            {'ref': 'xiao', 'marketplace_id': 3, 'tag': 'xiao_uk'},
            {'ref': 'xiao', 'marketplace_id': 4, 'tag': 'xiao_de'},
            {'ref': 'xiao', 'marketplace_id': 7, 'tag': 'xiao_ca'},
            {'ref': 'xiao', 'marketplace_id': 44551, 'tag': 'xiao_es'},
            {'ref': 'xiao', 'marketplace_id': 35691, 'tag': 'xiao_it'},
            {'ref': 'xiao', 'marketplace_id': 5, 'tag': 'xiao_fr'},
            {'ref': 'song', 'marketplace_id': 1, 'tag': 'song_us'},
            {'ref': 'song', 'marketplace_id': 3, 'tag': 'song_uk'},
            {'ref': 'song', 'marketplace_id': 4, 'tag': 'song_de'},
            {'ref': 'song', 'marketplace_id': 5, 'tag': 'song_fr'},
            {'ref': 'song', 'marketplace_id': 7, 'tag': 'song_ca'},
            {'ref': 'song', 'marketplace_id': 44551, 'tag': 'song_es'},
            {'ref': 'song', 'marketplace_id': 35691, 'tag': 'song_it'},
            {'ref': 'aceec', 'marketplace_id': 1, 'tag': 'aceec_us'},
            {'ref': 'aceec', 'marketplace_id': 3, 'tag': 'aceec_uk'},
            {'ref': 'aceec', 'marketplace_id': 4, 'tag': 'aceec_de'},
            {'ref': 'aceec', 'marketplace_id': 5, 'tag': 'aceec_fr'},
            {'ref': 'aceec', 'marketplace_id': 7, 'tag': 'aceec_ca'},
            {'ref': 'aceec', 'marketplace_id': 44551, 'tag': 'aceec_es'},
            {'ref': 'aceec', 'marketplace_id': 35691, 'tag': 'aceec_it'},
            ]
        for data in all_data:
            tag = EcspRefTag(ref=data['ref'],
                             marketplace_id=data['marketplace_id'],
                             tag=data['tag'])
            tag.add()


class AmzSaleFarmPrj(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_prjs'

    GC_NONE = 0
    GC_CUSTOMER = 1
    GC_ACEEC = 2

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    asin = Column(VARCHAR(16), nullable=False)
    merchant_name = Column(VARCHAR(256), nullable=False)
    path_to_asin = Column(JSONB)
    has_coupon = Column(BOOLEAN, default=True)
    gift_card_owner = Column(BIGINT, default=GC_NONE)
    actual_price = Column(BIGINT, default=0)  # min value is $0.01
    start_date = Column(BIGINT, default=make_date_period)
    plan = Column(JSONB)  # e.g. {date_period: order_cnt}
    order_cnt = Column(BIGINT, default=0)
    review_cnt = Column(BIGINT, default=0)
    has_address_cnt = Column(BIGINT, default=0)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzSaleFarmCoupon(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_coupons'

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT, default=0)
    coupon = Column(VARCHAR(64), default='')
    is_100_off = Column(BOOLEAN, default=True)
    buyer_id = Column(BIGINT, default=0)
    is_used = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzSaleFarmGiftCard(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_gift_cards'

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT, default=0)
    gift_card = Column(VARCHAR(64), default='')
    value = Column(BIGINT, default=0)  # min value is $0.01
    buyer_id = Column(BIGINT, default=0)
    is_used = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzSaleFarmReview(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_reviews'

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT, default=0)
    review_txt = Column(VARCHAR(65535))
    review_image = Column(JSONB)
    review_media = Column(JSONB)
    buyer_id = Column(BIGINT, default=0)
    reviewed_at = Column(TIMESTAMP(timezone=True))  # scheduled time
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzSaleFarmPrjTask(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_prj_tasks'

    _STATE_STOP = 0
    _STATE_INIT = 1
    _STATE_ADD_TO_CART = 2
    _STATE_ADD_TO_WISH = 3
    _STATE_ORDER_DONE = 4
    _STATE_SHIPMENT_DONE = 5
    _STATE_REVIEW_DONE = 6

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT, default=0)
    state = Column(BIGINT, default=_STATE_INIT)
    buyer_id = Column(BIGINT, default=0)
    order_no = Column(VARCHAR(64), default='')
    shipment_no = Column(VARCHAR(64), default='')
    scheduled_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    stopped_at = Column(TIMESTAMP(timezone=True))
    carted_at = Column(TIMESTAMP(timezone=True))
    wished_at = Column(TIMESTAMP(timezone=True))
    ordered_at = Column(TIMESTAMP(timezone=True))
    shipped_at = Column(TIMESTAMP(timezone=True))
    reviewed_at = Column(TIMESTAMP(timezone=True))


class AmzSaleFarmRealAddress(Base, BaseMethod):
    __tablename__ = 'amz_sale_farm_real_addresses'

    id = Column(BIGINT, primary_key=True)
    country = Column(VARCHAR(64), nullable=False)
    state = Column(VARCHAR(16), nullable=False)
    state_full = Column(VARCHAR(128))
    city = Column(VARCHAR(64), nullable=False)
    address_line1 = Column(VARCHAR(256), nullable=False)
    address_line2 = Column(VARCHAR(256))
    zip_code = Column(VARCHAR(16), nullable=False)
    used_by = Column(BIGINT, nullable=True)


class AmzGiftCard(Base, BaseMethod):
    __tablename__ = 'amz_gift_cards'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    gift_card = Column(VARCHAR(64), default='')
    value = Column(BIGINT, default=0)  # min value is $0.01
    provider = Column(VARCHAR(64), default='')
    is_used = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)


class EcspReviewerRole(Base, BaseMethod):
    __tablename__ = 'ecsp_reviewer_roles'

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(64))
    min_score = Column(BIGINT)
    max_score = Column(BIGINT)
    max_requests = Column(BIGINT)
    max_coupons = Column(BIGINT)

    @classmethod
    def default_data(cls):
        all_data = [
            {'name': 'silver', 'min_score': 0, 'max_score': 60,
             'max_requests': 30, 'max_coupons': 2},
            {'name': 'gold', 'min_score': 61, 'max_score': 150,
             'max_requests': 60, 'max_coupons': 10},
            {'name': 'platinum', 'min_score': 151, 'max_score': 510,
             'max_requests': 150, 'max_coupons': 40},
            {'name': 'diamond', 'min_score': 511, 'max_score': 9999,
             'max_requests': 9999, 'max_coupons': 150},
            ]
        for data in all_data:
            role = EcspReviewerRole(
                name=data['name'], min_score=data['min_score'],
                max_score=data['max_score'],
                max_requests=data['max_requests'],
                max_coupons=data['max_coupons'])
            role.add(commit=False)
        role.commit()

    @classmethod
    def get_role_by_score(cls, score):
        role = DBsession.query(cls).filter(cls.min_score <= score,
                                           cls.max_score >= score).first()
        if not role:
            return 1
        return role.id


class EcspReviewerScore(Base, BaseMethod):
    __tablename__ = 'ecsp_reviewer_scores'

    id = Column(BIGINT, primary_key=True)
    reviewer_role_id = Column(BIGINT, nullable=False)
    user_id = Column(BIGINT, nullable=False)
    score = Column(BIGINT, default=60)
    cur_requests = Column(BIGINT)
    cur_coupons = Column(BIGINT)
    lasting_bad_reviews = Column(BIGINT, default=1)

    @classmethod
    def query_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).first()

    def upgrade_demote_role(self, commit=True):
        self.reviewer_role_id = EcspReviewerRole.get_role_by_score(self.score)
        self.update(commit)


class AmzUserProfile(Base, BaseMethod):
    __tablename__ = 'amz_user_profiles'

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(512))
    email = Column(VARCHAR(512))
    user_id = Column(VARCHAR(512))
    reg_state = Column(BIGINT)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    JUST_LOGIN_AMAZON = 1
    REG_REVIEWER_SUCCESS = 2
    BIND_PROFILE_SUCCESS = 3

    @classmethod
    def get_by_email(cls, email):
        return DBsession.query(cls).filter(cls.email == email).first()


class EcspUserWechatRelation(Base, BaseMethod):
    __tablename__ = 'ecsp_user_wechat_relations'
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    wechat_id = Column(VARCHAR(512), nullable=False)

    @classmethod
    def query_wechat_id_by_user_id(cls, user_id):
        return DBsession.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def save(cls, user_id, wechat_id):
        if not user_id or not wechat_id:
            return

        obj = DBsession.query(cls).filter(
            cls.user_id == user_id, cls.wechat_id == wechat_id).first()
        if not obj:
            obj = EcspUserWechatRelation(user_id=user_id, wechat_id=wechat_id)
            obj.add()

    @classmethod
    def remove(cls, wechat_id):
        if not wechat_id:
            return

        objs = DBsession.query(cls).filter(cls.wechat_id == wechat_id).all()
        if not objs:
            return

        for obj in objs:
            obj.delete(commit=False)
        cls.commit()


class AmzKwRankImprPrjLog(Base, BaseMethod):
    __tablename__ = 'amz_kw_rank_impr_prj_logs'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    market_place_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    keywords = Column(VARCHAR(512), nullable=False)
    quantity = Column(BIGINT)
    is_accelerated = Column(BOOLEAN)
    state = Column(BIGINT)
    impr_type = Column(BIGINT)
    group_desc = Column(VARCHAR(128), default='aps')
    started_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    stoped_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

    START = 1
    STOP = 2
    CART_FARMING = 1
    DYNAMIC_SUPERURL = 2

    @classmethod
    def get_by_user_asin_kws_type_group(cls, user_id, market_id, asin,
                                        keywords, impr_type, group_desc):
        return DBsession.query(cls).filter(cls.user_id == user_id,
                                           cls.market_place_id == market_id,
                                           cls.asin == asin,
                                           cls.keywords == keywords,
                                           cls.group_desc == group_desc,
                                           cls.impr_type == impr_type).all()

    @classmethod
    def get_last_started_log(cls, user_id, market_id, asin, keywords,
                             impr_type, group_desc):
        return DBsession.query(cls).\
            filter(cls.user_id == user_id, cls.market_place_id == market_id,
                   cls.asin == asin, cls.keywords == keywords,
                   cls.state == cls.START,
                   cls.group_desc == group_desc,
                   cls.impr_type == impr_type).\
            order_by(cls.started_at.desc()).first()

    def stop(self, commit=True):
        self.state = self.STOP
        return self.update(commit)


class AmzAsinVariants(Base, BaseMethod):
    __tablename__ = 'amz_asin_variants'

    id = Column(BIGINT, primary_key=True)
    parent_asin = Column(VARCHAR(32), nullable=False)
    child_asin = Column(VARCHAR(32), nullable=False)
    marketplace_id = Column(BIGINT, nullable=False)

    @classmethod
    def get_by_market_child_asin(cls, marketplace_id, child_asin):
        return DBsession.query(cls).\
            filter(cls.child_asin == child_asin,
                   cls.marketplace_id == marketplace_id).first()

    @classmethod
    def delete_same_parent_asins(cls, child_asin, marketplace_id, commit=True):
        child = cls.get_by_market_child_asin(marketplace_id, child_asin)
        if not child:
            return False

        all_children = DBsession.query(cls).\
            filter(cls.parent_asin == child.parent_asin,
                   cls.marketplace_id == marketplace_id).all()
        for children in all_children:
            children.delete(commit=False)

        return True if not commit else BaseMethod.commit()

    @classmethod
    def save_asins_with_parent(cls, parent_asin, asins, marketplace_id,
                               commit=True):
        for asin in asins:
            obj = AmzAsinVariants(parent_asin=parent_asin, child_asin=asin,
                                  marketplace_id=marketplace_id)
            obj.add(commit=False)

        return True if not commit else BaseMethod.commit()

    @classmethod
    def get_same_parent_asins(cls, child_asin, marketplace_id):
        child = DBsession.query(cls).\
            filter(cls.child_asin == child_asin,
                   cls.marketplace_id == marketplace_id).first()
        if not child:
            return []

        all_children = DBsession.query(cls).\
            filter(cls.parent_asin == child.parent_asin,
                   cls.marketplace_id == marketplace_id).all()

        return [x.child_asin for x in all_children]


class AmzLongTailKeyword(Base, BaseMethod):
    __tablename__ = 'amz_long_tail_keywords'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    keywords = Column(VARCHAR(65535), nullable=False)
    parent_keywords = Column(VARCHAR(65535))
    month_period = Column(BIGINT, default=make_month_period)
    hot = Column(BIGINT, nullable=False)
    group_desc = Column(VARCHAR(256), default='aps')

    @classmethod
    def query_long_tail_keywords(cls, parent_keywords, marketplace_id,
                                 group_desc='aps'):
        month_period = make_month_period()
        return DBsession.query(cls).\
            filter(cls.parent_keywords == parent_keywords,
                   cls.marketplace_id == marketplace_id,
                   cls.group_desc == group_desc,
                   cls.month_period == month_period).first()

    @classmethod
    def _query_all_kw_with_parent_kw(cls, marketplace_id, group_desc, keywords,
                                     limit=10,
                                     month_period=make_month_period()):
        return DBsession.query(cls).\
            filter(cls.parent_keywords == keywords,
                   cls.marketplace_id == marketplace_id,
                   cls.group_desc == group_desc,
                   cls.month_period == month_period).limit(limit).all()

    @classmethod
    def save_long_tail_keywords(cls, keywords, marketplace_id,
                                group_desc='aps', parent_keywords=None,
                                hot=0, commit=True):
        kw = cls.query_all_kw_with_parent_kw(marketplace_id, group_desc,
                                             keywords)
        if kw:
            return False

        month_period = make_month_period()
        kw = AmzLongTailKeyword(keywords=keywords,
                                marketplace_id=marketplace_id,
                                parent_keywords=parent_keywords,
                                month_period=month_period,
                                hot=hot)
        kw.add(commit=commit)
        return True if not commit else BaseMethod.commit()

    @classmethod
    def query_all_kw_with_parent_kw(cls, marketplace_id, group_desc, keywords,
                                    limit=10):
        month_period = make_month_period()
        return cls._query_all_kw_with_parent_kw(marketplace_id, group_desc,
                                                keywords, limit, month_period)

    @classmethod
    def query_all_kw_with_parent_kw_last_month(cls, marketplace_id, group_desc,
                                               keywords, limit=10):
        last_month = make_last_month_period()
        return cls._query_all_kw_with_parent_kw(marketplace_id, group_desc,
                                                keywords, limit, last_month)


class AmzLongTailFailureKeyword(Base, BaseMethod):
    __tablename__ = 'amz_long_tail_failure_keywords'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    keywords = Column(VARCHAR(65535), nullable=False)
    month_period = Column(BIGINT, default=make_month_period)
    failure_type = Column(VARCHAR(16), default='keywords')

    @classmethod
    def query_failure_keywords(cls, marketplace_id, keywords, month_period,
                               failure_type='keywords'):
        return DBsession.query(cls).\
            filter(cls.marketplace_id == marketplace_id,
                   cls.keywords == keywords,
                   cls.month_period == month_period,
                   cls.failure_type == keywords).first()

    @classmethod
    def save_failure_keywords(cls, marketplace_id, keywords,
                              month_period=None, failure_type='keywords'):
        if not month_period:
            month_period = make_month_period()

        failure_kw = cls.query_failure_keywords(marketplace_id, keywords,
                                                month_period,
                                                failure_type)
        if failure_kw:
            return True

        failure_kw = AmzLongTailFailureKeyword(marketplace_id=marketplace_id,
                                               keywords=keywords,
                                               month_period=month_period,
                                               failure_type=failure_type)
        return failure_kw.add()


class AmzNewSuperurlTestLog(Base, BaseMethod):
    __tablename__ = 'amz_new_superurl_test_logs'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    asin = Column(VARCHAR(64), nullable=False)
    keywords = Column(VARCHAR(65535), nullable=False)
    brand = Column(VARCHAR(64))
    referer = Column(VARCHAR(512))
    test_type = Column(BIGINT)
    used_time = Column(REAL, default=0.0)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class AmzKeywordsNode(Base, BaseMethod):
    __tablename__ = 'amz_keywords_nodes'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT)
    keywords = Column(VARCHAR(65535), nullable=False)
    nodes_name = Column(VARCHAR(65535), nullable=False)
    nodes_alias = Column(VARCHAR(65535), nullable=False)
    month_period = Column(BIGINT, default=make_month_period)

    @classmethod
    def query_keyword_nodes_by_month(cls, marketplace_id, keywords,
                                     month_period=make_month_period()):
        return DBsession.query(cls).\
            filter(cls.marketplace_id == marketplace_id,
                   cls.keywords == keywords,
                   month_period == month_period).first()

    @classmethod
    def query_keyword_nodes_by_alias(cls, marketplace_id, keywords,
                                     nodes_alias,
                                     month_period=make_month_period()):
        return DBsession.query(cls).\
            filter(cls.marketplace_id == marketplace_id,
                   cls.keywords == keywords,
                   cls.nodes_alias == nodes_alias,
                   month_period == month_period).first()

    @classmethod
    def save_keywords_nodes(cls, marketplace_id, keywords, nodes_name,
                            nodes_alias, month_period=make_month_period(),
                            commit=False):

        kw_nodes = cls.query_keyword_nodes_by_alias(marketplace_id, keywords,
                                                    nodes_alias,
                                                    month_period)

        if kw_nodes:
            return False

        kw_nodes = AmzKeywordsNode(marketplace_id=marketplace_id,
                                   keywords=keywords,
                                   nodes_name=nodes_name,
                                   nodes_alias=nodes_alias,
                                   month_period=month_period)
        return kw_nodes.add(commit=commit)


class AmzKwRankImprPrjParam(Base, BaseMethod):
    __tablename__ = 'amz_kw_rank_impr_prj_params'

    URL_TYPE_0 = 0
    URL_TYPE_1 = 1
    URL_TYPE_2 = 2
    URL_TYPE_3 = 3
    URL_TYPE_4 = 4

    id = Column(BIGINT, primary_key=True)
    prj_id = Column(BIGINT)
    url_type = Column(BIGINT, nullable=False, default=URL_TYPE_0)
    url_params = Column(JSONB)

    @classmethod
    def save_url_type(cls, prj_id, url_params={}, commit=True):
        prj_param = DBsession.query(cls).filter(cls.prj_id == prj_id).first()
        if prj_param:
            return True

        prj_param = AmzKwRankImprPrjParam(prj_id=prj_id,
                                          url_params=url_params)
        return prj_id.add(commit=commit)

    @classmethod
    def query_prj_param_by_prj_id(cls, prj_id):
        prj_param = DBsession.query(cls).filter(cls.prj_id == prj_id).first()
        if prj_param:
            return prj_param

        prj_param = AmzKwRankImprPrjParam(prj_id=prj_id)
        prj_param.add()
        return prj_param if prj_param.add() else None

    @classmethod
    def get_url_type_by_prj_id(cls, prj_id):
        prj_param = cls.query_prj_param_by_prj_id(prj_id)
        return prj_param.url_type if prj_param else cls.URL_TYPE_0


class AmzAccountCreatedList(Base, BaseMethod):
    __tablename__ = 'amz_account_created_lists'

    TYPE_WISH_LIST = 0
    TYPE_SHOPPING_LIST = 1
    TYPE_GIFT_LIST = 2

    PRIVACY_PUBLIC = 0
    PRIVACY_PRIVATE = 1
    PRIVACY_SHARED = 2

    id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, ForeignKey('amz_account_infos.id'))
    marketplace_id = Column(BIGINT, nullable=False, default=1)
    name = Column(VARCHAR(128), nullable=False)
    list_token = Column(VARCHAR(64), default='')
    list_type = Column(BIGINT, nullable=False, default=TYPE_WISH_LIST)
    privacy = Column(BIGINT, nullable=False, default=PRIVACY_PUBLIC)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP(timezone=True))
    is_available = Column(BOOLEAN, default=False)

    @classmethod
    def get_list_by_account_market_type_name(
            cls, account_id, marketplace_id, name, list_type=TYPE_WISH_LIST):
        return DBsession.query(cls).filter(
            cls.account_id == account_id,
            cls.marketplace_id == marketplace_id,
            cls.list_type == list_type,
            cls.name == name,
            cls.is_available.is_(True)).first()

    @classmethod
    def get_list_by_account_market_type_token(
            cls, account_id, marketplace_id, token, list_type=TYPE_WISH_LIST):
        return DBsession.query(cls).filter(
            cls.account_id == account_id,
            cls.marketplace_id == marketplace_id,
            cls.list_type == list_type,
            cls.token == token,
            cls.is_available.is_(True)).first()

    @classmethod
    def save(cls, account_id, marketplace_id, name, list_token, list_type,
             privacy):
        obj = AmzAccountCreatedList.get_list_by_account_market_type_name(
            account_id, marketplace_id, name)
        if not obj:
            obj = AmzAccountCreatedList(
                account_id=account_id,
                marketplace_id=marketplace_id,
                name=name,
                list_token=list_token,
                list_type=list_type,
                privacy=privacy,
                is_available=True)
            obj.add()

        return obj

    def delete(self, commit=True):
        self.deleted_at = datetime.utcnow()
        self.is_available = False
        self.update(commit=False)
        if commit:
            self.commit()

        return True

    def set_list_unavailable(self):
        self.is_available = False
        self.update()
        list_info_ins = AmzAccountListInfo.get_by_account_market(
            self.account_id, self.marketplace_id)
        wish_list_ids = [l for l in list_info_ins.available_list_array]
        wish_list_ids.remove(self.id)
        list_info_ins.update()


class AmzAsinInList(Base, BaseMethod):
    __tablename__ = 'amz_asin_in_lists'

    LIST_ITEM_MAX = 99

    id = Column(BIGINT, primary_key=True)
    asin = Column(VARCHAR(16), nullable=False)
    marketplace_id = Column(BIGINT, nullable=False)
    keywords = Column(VARCHAR(512))
    list_id = Column(BIGINT, ForeignKey('amz_account_created_lists.id'))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP(timezone=True), default=None)

    @classmethod
    def is_asin_in_list(cls, asin, marketplace_id, list_id):
        item = DBsession.query(cls).filter(
            cls.asin == asin, cls.marketplace_id == marketplace_id,
            cls.list_id == list_id, cls.deleted_at.is_(None)).first()
        return False if not item else True

    @classmethod
    def save(cls, asin, marketplace_id, keywords, list_id):
        AmzAsinInList(asin=asin.upper(), marketplace_id=marketplace_id,
                      keywords=keywords.lower(), list_id=list_id).add()
        count = DBsession.query(cls).filter(cls.list_id == list_id,
                                            cls.deleted_at.is_(None)).count()
        if count >= cls.LIST_ITEM_MAX:
            list_instance = AmzAccountCreatedList.get_by_id(list_id)
            list_instance.set_list_unavailable()


class AmzAccountListInfo(Base, BaseMethod):
    __tablename__ = 'amz_account_list_infos'
    id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, ForeignKey('amz_account_infos.id'))
    marketplace_id = Column(BIGINT, default=1)
    available_list_array = Column(ARRAY(Integer))
    default_list_id = Column(BIGINT, default=0)

    @classmethod
    def get_by_account_market(cls, account_id, marketplace_id):
        return DBsession.query(cls).filter(
            cls.account_id == account_id,
            cls.marketplace_id == marketplace_id).first()

    @classmethod
    def save(cls, account_id, marketplace_id, list_ids):
        obj = AmzAccountListInfo(
            account_id=account_id, marketplace_id=marketplace_id,
            available_list_array=list_ids)
        obj.add()

        return obj



#进行ORM映射时，sqlalchemy要求第一个参数为Base
#第二参数为基类方法
class AmzMWSAccount(Base, BaseMethod):
    __tablename__ = 'amz_mws_accounts'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, default=1)
    name = Column(VARCHAR(32), nullable=False)
    merchant_id = Column(VARCHAR(16), nullable=False)
    key = Column(VARCHAR(32), nullable=False)
    secret = Column(VARCHAR(64), nullable=False)

    @classmethod
    def get_by_market_name(cls, marketplace_id, name):
        return DBsession.query(cls).filter(
            cls.marketplace_id == marketplace_id,
            cls.name == name).first()


class AmzReportRequest(Base, BaseMethod):
    __tablename__ = 'amz_report_requests'

    ST_SUBMITTED = '_SUBMITTED_'
    ST_IN_PROGRESS = '_IN_PROGRESS_'
    ST_CANCELLED = '_CANCELLED_'
    ST_DONE = '_DONE_'
    ST_DONE_NO_DATA = '_DONE_NO_DATA_'
    ST_DOWNLOADED = 'DOWNLOADED'

    _ongoing_status = [ST_SUBMITTED, ST_IN_PROGRESS]

    ALL_ORDER = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_'
    FBA_ORDER = '_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_'
    FBM_ORDER = '_GET_FLAT_FILE_ORDERS_DATA_'

    FBA_INVENTORY = '_GET_AFN_INVENTORY_DATA_'
    RESERVED_SKU = '_GET_RESERVED_INVENTORY_DATA_'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, default=1)
    name = Column(VARCHAR(32), nullable=False)
    rep_type = Column(VARCHAR(64), nullable=False)
    request_id = Column(VARCHAR(64), nullable=False)
    report_id = Column(VARCHAR(64), nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=True)
    end_date = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(VARCHAR(64), default=ST_SUBMITTED)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)


    #查询亚马逊后台报表结果
    @classmethod
    def get_request(cls, market_id, name, rep_type, start_date, end_date):
        return DBsession.query(cls).filter(cls.marketplace_id == market_id,
                                           cls.name == name,
                                           cls.rep_type == rep_type,
                                           cls.start_date == start_date,
                                           cls.end_date == end_date)\
                                   .first()


    #查询已经已经提交或正在生成的报表
    @classmethod
    def find_ongoing_report(cls):
        return DBsession.query(cls)\
            .filter(cls.status.in_(cls._ongoing_status))\
            .all()

    @classmethod
    def find_ready_report(cls):
        return DBsession.query(cls).filter(cls.report_id != '',
                                           cls.status == cls.ST_DONE).all()

    #判断亚马逊报表状态：
    #已经生成、没数据、可下载
    def is_done(self):
        return self.status in [AmzReportRequest.ST_DONE,
                               AmzReportRequest.ST_DONE_NO_DATA,
                               AmzReportRequest.ST_DOWNLOADED]

    def is_cancelled(self):
        return self.status == AmzReportRequest.ST_CANCELLED

    def downloaded(self, commit=True):
        self.status = AmzReportRequest.ST_DOWNLOADED
        self.update(commit)


class AmzReport(BaseMethod):
    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, default=1)
    name = Column(VARCHAR(32), nullable=False)

    @staticmethod
    def mk_datetime(str_value):
        if not str_value:
            return None

        return datetime.strptime(str_value[:19], '%Y-%m-%dT%H:%M:%S')\
                       .replace(tzinfo=pytz.UTC)

    @staticmethod
    def convert(clz, obj, rep_type, json_data):
        valid_fields = clz.get_valid_fields(rep_type)
        if not valid_fields:
            return

        for k, v in json_data.items():
        #python3将dict中的iteritems换成items
        #for k, v in json_data.iteritems():
            if not v:
                continue

            field_name = valid_fields.get(k, '')
            if not field_name:
                continue

            if not hasattr(obj, field_name):
                continue

            field = getattr(clz, field_name)
            if isinstance(field, BIGINT):
                setattr(obj, field_name, int(v))
            elif isinstance(field, REAL):
                setattr(obj, field_name, float(v))
            elif isinstance(field, TIMESTAMP):
                setattr(obj, field_name, AmzReport.mk_datetime(v))
            #setattr(obj, field_name, v.decode('iso8859-1').encode('utf-8'))
            #setattr(obj, field_name, v.encode('utf-8'))
            setattr(obj, field_name, v)

class AmzSellerOrder(Base, AmzReport):
    __tablename__ = 'amz_seller_orders'

    amazon_order_id = Column(VARCHAR(32), nullable=False)
    merchant_order_id = Column(VARCHAR(32))
    purchase_date = Column(TIMESTAMP(timezone=True))
    payments_date = Column(TIMESTAMP(timezone=True))
    last_updated_date = Column(TIMESTAMP(timezone=True))
    order_status = Column(VARCHAR(32))
    fulfillment_channel = Column(VARCHAR(32))
    sales_channel = Column(VARCHAR(32))
    ship_service_level = Column(VARCHAR(64))
    sku = Column(VARCHAR(32))
    # product_name = Column(VARCHAR(256))
    asin = Column(VARCHAR(16))
    item_status = Column(VARCHAR(32))
    quantity = Column(BIGINT, default=0)
    currency = Column(VARCHAR(8))
    item_price = Column(REAL, default=0.0)
    item_tax = Column(REAL, default=0.0)
    shipping_price = Column(REAL, default=0.0)
    ship_tax = Column(REAL, default=0.0)
    gift_wrap_price = Column(REAL, default=0.0)
    gift_wrap_tax = Column(REAL, default=0.0)
    item_promotion_discount = Column(REAL, default=0.0)
    ship_promotion_discount = Column(REAL, default=0.0)
    promotion_ids = Column(VARCHAR(256))
    buyer_email = Column(VARCHAR(64))
    buyer_name = Column(VARCHAR(64))
    buyer_phone_number = Column(VARCHAR(32))
    delivery_start_date = Column(TIMESTAMP(timezone=True))
    delivery_end_date = Column(TIMESTAMP(timezone=True))
    delivery_time_zone = Column(VARCHAR(32))
    delivery_instructions = Column(VARCHAR(256))

    _report_map = {
        AmzReportRequest.ALL_ORDER: {
            'amazon_order_id': 'amazon_order_id',
            'merchant_order_id': 'merchant_order_id',
            'purchase_date': 'purchase_date',
            'last_updated_date': 'last_updated_date',
            'order_status': 'order_status',
            'fulfillment_channel': 'fulfillment_channel',
            'sales_channel': 'sales_channel',
            'ship_service_level': 'ship_service_level',
            'sku': 'sku',
            # 'product_name': 'product_name',
            'asin': 'asin',
            'item_status': 'item_status',
            'quantity': 'quantity',
            'currency': 'currency',
            'item_price': 'item_price',
            'item_tax': 'item_tax',
            'shipping_price': 'shipping_price',
            'ship_tax': 'ship_tax',
            'gift_wrap_price': 'gift_wrap_price',
            'gift_wrap_tax': 'gift_wrap_tax',
            'item_promotion_discount': 'item_promotion_discount',
            'ship_promotion_discount': 'ship_promotion_discount',
            'promotion_ids': 'promotion_ids',
            },
        AmzReportRequest.FBM_ORDER: {
            'payments_date': 'payments_date',
            'buyer_email': 'buyer_email',
            'buyer_name': 'buyer_name',
            'buyer_phone_number': 'buyer_phone_number',
            'delivery_start_date': 'delivery_start_date',
            'delivery_end_date': 'delivery_end_date',
            'delivery_time_zone': 'delivery_time_zone',
            'delivery_instructions': 'delivery_instructions',
            },
        AmzReportRequest.FBA_ORDER: {
            'payments_date': 'payments_date',
            'buyer_email': 'buyer_email',
            'buyer_name': 'buyer_name',
            'buyer_phone_number': 'buyer_phone_number',
            },
        }



    @classmethod
    def get_report_types(cls):
        return [AmzReportRequest.ALL_ORDER, AmzReportRequest.FBA_ORDER,
                AmzReportRequest.FBM_ORDER]

    @classmethod
    def get_valid_fields(cls, rep_type):
        return cls._report_map.get(rep_type, None)

    @classmethod
    def get_by_market_orders(cls, market_id, order_id):
        return DBsession.query(cls).filter(
            cls.marketplace_id == market_id,
            cls.amazon_order_id == order_id).all()

    @classmethod
    def get_by_market_order_sku(cls, market_id, order_id, sku):
        return DBsession.query(cls).filter(
            cls.marketplace_id == market_id,
            cls.amazon_order_id == order_id,
            cls.sku == sku).first()

    @classmethod
    def save(cls, market_id, name, rep_type, json_data, commit=False):
        def _save_all_order():
            order = AmzSellerOrder.get_by_market_order_sku(
                market_id,
                json_data.get('amazon_order_id'),
                json_data.get('sku'))

            if not order:
                order = AmzSellerOrder(marketplace_id=market_id, name=name)
                AmzReport.convert(cls, order, rep_type, json_data)
                order.add(commit=commit)
                return

            AmzReport.convert(cls, order, rep_type, json_data)
            order.update(commit=commit)

        def _save_fba_fbm_order():
            if not json_data.get('amazon_order_id') and \
               rep_type == AmzReportRequest.FBM_ORDER:
                json_data['amazon_order_id'] = json_data.get('order_id')

            order = AmzSellerOrder.get_by_market_order_sku(
                market_id,
                json_data.get('amazon_order_id'),
                json_data.get('sku'))
            if not order:
                log.error('You must import all orders before saving %s, %s' % (
                    rep_type, json_data))
                return

            AmzReport.convert(cls, order, rep_type, json_data)
            order.update(commit=commit)

        if rep_type == AmzReportRequest.ALL_ORDER:
            _save_all_order()
            return

        _save_fba_fbm_order()

    @classmethod
    def query_recent_saled_units_per_chanel_asin(cls, market_id, name,
                                                 now=datetime.utcnow(),
                                                 days=7):
        sql_tmpl = '''
SELECT
    sales_channel, asin, sku,
    to_char(purchase_date, 'YYYYMMDD') dt,
    sum(quantity) AS qty
FROM amz_seller_orders
WHERE marketplace_id = {market_id} AND name='{name}'
AND purchase_date BETWEEN to_date('{start_date}', 'YYYYMMDD')
    AND to_date('{end_date}', 'YYYYMMDD')
AND fulfillment_channel!='Merchant'
AND order_status not in ('Cancelled')
AND item_status not in ('Cancelled')
GROUP BY sales_channel, asin, sku, to_char(purchase_date, 'YYYYMMDD')
ORDER BY asin, sku, sales_channel;
        '''

        def _formate_date(d):
            return d.strftime('%Y%m%d')

        start_date = _formate_date(now - timedelta(days=days))
        end_date = _formate_date(now)

        return fetchall(sql_tmpl.format(market_id=market_id,
                                        name=name,
                                        start_date=start_date,
                                        end_date=end_date))

    @classmethod
    def query_data_per_chanel_at_specific_date(cls, market_id, name,
                                               specific_date):
        end_date = specific_date + timedelta(days=1)

        return cls.query_recent_saled_units_per_chanel_asin(market_id, name,
                                                            now=end_date,
                                                            days=1)

    @classmethod
    def query_recent_saled_units_per_asin(cls, market_id, name,
                                          now=datetime.utcnow(), days=7):
        sql_tmpl = '''
SELECT
    asin, sku,
    to_char(purchase_date, 'YYYYMMDD') dt,
    sum(quantity) AS qty
FROM amz_seller_orders
WHERE marketplace_id = {market_id} AND name='{name}'
AND purchase_date BETWEEN to_date('{start_date}', 'YYYYMMDD')
    AND to_date('{end_date}', 'YYYYMMDD')
AND fulfillment_channel!='Merchant'
AND order_status not in ('Cancelled')
AND item_status not in ('Cancelled')
GROUP BY asin, sku, to_char(purchase_date, 'YYYYMMDD')
ORDER BY asin, sku;
        '''

        def _formate_date(d):
            return d.strftime('%Y%m%d')

        start_date = _formate_date(now - timedelta(days=days))
        end_date = _formate_date(now)

        return fetchall(sql_tmpl.format(market_id=market_id,
                                        name=name,
                                        start_date=start_date,
                                        end_date=end_date))

    @classmethod
    def query_data_at_specific_date(cls, market_id, name, specific_date):
        end_date = specific_date + timedelta(days=1)

        return cls.query_recent_saled_units_asin(market_id, name,
                                                 now=end_date, days=1)

    def get_contact(self):
        if self.buyer_email:
            return self.buyer_name, self.buyer_email
        if self.sales_channel != 'Non-Amazon' or not self.merchant_order_id:
            return None, None

        # multiple channel orders
        order_id = self.merchant_order_id[:19]
        orders = AmzSellerOrder.get_by_market_orders(self.marketplace_id,
                                                     order_id)
        if not orders:
            return None, None

        return orders[0].buyer_name, orders[0].buyer_email

#-----------------

        


    @classmethod
    def query_latest_week_average_daily_orders_qty(cls):
        return DBsession.query(cls.marketplace_id,
                             cls.name,
                             cls.asin,
                             cls.sku,
                             (func.sum(cls.quantity)/7).label("average_orders_qty")
                            ).filter(and_(cls.purchase_date.between((func.current_timestamp()-timedelta(days=7)),
                                         (func.current_timestamp()-timedelta(days=0))),
                                          cls.fulfillment_channel=="Amazon",
                                          cls.sales_channel != 'Non-Amazon'
                                          )
                            ).group_by(cls.marketplace_id,cls.asin,cls.name,cls.sku).all()

    @classmethod
    def query_average_daily_orders_qty(cls):
        sql_tmpl = '''
WITH last_week as(
SELECT 
    marketplace_id,name,asin,sku,
    SUM(quantity)/7 AS quantity
FROM amz_seller_orders
WHERE purchase_date BETWEEN CURRENT_DATE-7 AND CURRENT_DATE
    AND fulfillment_channel = 'Amazon'
    AND sales_channel != 'Non-Amazon'
GROUP BY marketplace_id,asin,name,asin,sku
),last_but_two_three_week as(
SELECT 
    marketplace_id,name,asin,sku,
    SUM(quantity)/14 AS quantity
FROM amz_seller_orders
WHERE purchase_date BETWEEN CURRENT_DATE-21 AND CURRENT_DATE-7
    AND fulfillment_channel = 'Amazon'
    AND sales_channel != 'Non-Amazon'
GROUP BY marketplace_id,asin,name,asin,sku
),last_but_one_month as (
SELECT 
    marketplace_id,name,asin,sku,
    SUM(quantity)/30 AS quantity
FROM amz_seller_orders
WHERE purchase_date BETWEEN CURRENT_DATE-51 AND CURRENT_DATE-21
    AND fulfillment_channel = 'Amazon'
    AND sales_channel != 'Non-Amazon'
GROUP BY marketplace_id,asin,name,asin,sku
)
SELECT last_week.marketplace_id,last_week.name,last_week.asin,last_week.sku,
    last_week.quantity AS last_week_quantity,
    last_but_two_three_week.quantity AS fortnight_quantity,
    last_but_one_month.quantity AS month_quantity
FROM last_week 
LEFT JOIN  last_but_two_three_week ON(
last_week.marketplace_id = last_but_two_three_week.marketplace_id
AND last_week.name = last_but_two_three_week.name
AND last_week.asin = last_but_two_three_week.asin
AND last_week.sku = last_but_two_three_week.sku
)LEFT JOIN last_but_one_month ON(
last_but_two_three_week.marketplace_id = last_but_one_month.marketplace_id
AND last_but_two_three_week.name = last_but_one_month.name
AND last_but_two_three_week.asin = last_but_one_month.asin
AND last_but_two_three_week.sku = last_but_one_month.sku
)
ORDER BY last_week.marketplace_id ASC,last_week.name

                '''
        return fetchall(sql_tmpl)



    @classmethod
    def oreder_asin_not_in_watched_asin(cls):

        ASIN_IN_WATCHED_ASIN = DBsession.query(AmzWatchedAsin.asin).subquery()
        return DBsession.query(cls.marketplace_id,
                                cls.asin,
                                cls.sales_channel,
                                cls.fulfillment_channel
                              ).filter(and_((cls.asin not in ASIN_IN_WATCHED_ASIN),
                                             cls.fulfillment_channel != 'Merchant') 
                              ).group_by(cls.marketplace_id,
                                         cls.asin,
                                         cls.sales_channel,
                                         cls.fulfillment_channel
                              ).order_by(desc(cls.marketplace_id))

    @classmethod
    def get_monthly_sales_info(cls):
        QtySales = DBsession.query((AmzMarketplace.id).label('marketplace_id'),
                                   cls.asin,
                                   cls.sku,
                                   func.sum(cls.quantity).label('quantity'),
                                   func.sum(cls.item_price).label('sales'),
                                   func.sum(cls.item_price*0.15).label('total_commission'),
                                   func.substr(cls.sales_channel,8,9).label('station')
                                   ).filter(and_(func.substr(cls.sales_channel,8,9) == func.substr(AmzMarketplace.website,12,16),
                                                cls.fulfillment_channel == 'Amazon',
                                                cls.order_status == 'Shipped',
                                                cls.purchase_date.between('2017-10-01','2017-11-01')
                                                )
                                   ).group_by(AmzMarketplace.id,cls.asin,cls.sku,
                                              func.substr(cls.sales_channel,8,9).label('station')
                                   ).order_by(asc(AmzMarketplace.id)
                                   ).subquery()
        return DBsession.query(QtySales.c.marketplace_id,
                               QtySales.c.asin,
                               QtySales.c.sku,
                               AmzCostFeeLog.fba_fulfilment_fee_per_unit,
                               QtySales.c.quantity,
                               QtySales.c.sales,
                               QtySales.c.total_commission,
                               func.sum(QtySales.c.quantity*AmzCostFeeLog.fba_fulfilment_fee_per_unit).label('total_fba_fulfilment_fee'),
                               QtySales.c.station
                              ).outerjoin(AmzCostFeeLog,
                                          and_(AmzCostFeeLog.marketplace_id == QtySales.c.marketplace_id,
                                               AmzCostFeeLog.asin == QtySales.c.asin,
                                               AmzCostFeeLog.sku == QtySales.c.sku
                                              )
                              ).group_by(QtySales.c.marketplace_id,
                                         QtySales.c.asin,
                                         QtySales.c.sku,
                                         AmzCostFeeLog.fba_fulfilment_fee_per_unit,
                                         QtySales.c.quantity,
                                         QtySales.c.sales,
                                         QtySales.c.total_commission,
                                         QtySales.c.station
                              ).order_by(asc(QtySales.c.marketplace_id)
                              ).all()
    @classmethod
    def get_buyer_email_by_payments_last_day(cls):
        return DBsession.query(cls).filter(and_(cls.payments_date.between(func.current_date()-timedelta(days=1),func.current_date()-timedelta(days=0)),
                                                cls.fulfillment_channel == 'Amazon',
                                                #cls.order_status == 'Shipped',
                                                #cls.item_status == 'Shipped',
                                                #cls.payments_date.between('2017-12-08 00:04:21+00','2017-12-08 11:39:00+00')
                                                #以下两条仅为测试用
                                                # cls.amazon_order_id == '404-1645955-5349145',
                                                # cls.sales_channel == 'Amazon.it'
                                                )
                                          ).order_by(asc(cls.sales_channel),desc(cls.payments_date)
                                          ).all()


class AmzSellerOrderAddress(Base, AmzReport):
    __tablename__ = 'amz_seller_order_addresses'

    amazon_order_id = Column(VARCHAR(32), nullable=False)
    recipient_name = Column(VARCHAR(256))
    ship_address_1 = Column(VARCHAR(256))
    ship_address_2 = Column(VARCHAR(256))
    ship_address_3 = Column(VARCHAR(256))
    ship_city = Column(VARCHAR(64))
    ship_state = Column(VARCHAR(64))
    ship_postal_code = Column(VARCHAR(16))
    ship_country = Column(VARCHAR(16))
    ship_phone_number = Column(VARCHAR(32))


class AmzFbaInvInfo(Base, AmzReport):
    __tablename__ = 'amz_fba_inv_infos'

    CT_NEW = 'NewItem'
    WCC_SELLABLE = 'SELLABLE'
    WCC_UNSELLABLE = 'UNSELLABLE'

    asin = Column(VARCHAR(16))
    sku = Column(VARCHAR(32))
    fnsku = Column(VARCHAR(32))
    condition_type = Column(VARCHAR(16), default=CT_NEW)
    warehouse_condition_code = Column(VARCHAR(16), default=WCC_SELLABLE)
    date_period = Column(BIGINT, default=make_date_period)
    quantity_available = Column(BIGINT, default=0)
    reserved_qty = Column(BIGINT, default=0)
    reserved_customerorders = Column(BIGINT, default=0)
    reserved_fc_transfers = Column(BIGINT, default=0)
    reserved_fc_processing = Column(BIGINT, default=0)

    _report_map = {
        AmzReportRequest.FBA_INVENTORY: {
            'seller_sku': 'sku',
            'fulfillment_channel_sku': 'fnsku',
            'asin': 'asin',
            'condition_type': 'last_updated_date',
            'warehouse_condition_code': 'warehouse_condition_code',
            'quantity_available': 'quantity_available',
            },
        AmzReportRequest.RESERVED_SKU: {
            'sku': 'sku',
            'fnsku': 'fnsku',
            'asin': 'asin',
            'reserved_qty': 'reserved_qty',
            'reserved_customerorders': 'reserved_customerorders',
            'reserved_fc_transfers': 'reserved_fc_transfers',
            'reserved_fc_processing': 'reserved_fc_processing',
            },
    }

    @classmethod
    def get_report_types(cls):
        return [AmzReportRequest.FBA_INVENTORY, AmzReportRequest.RESERVED_SKU]

    @classmethod
    def get_valid_fields(cls, rep_type):
        return cls._report_map.get(rep_type, None)

    @classmethod
    def query_recent_inventory_per_sku(cls, market_id, name,
                                       now=datetime.utcnow(), days=7):
        sql_tmpl = '''
SELECT asin, sku, date_period,
    SUM(quantity_available + reserved_qty) AS qty
FROM amz_fba_inv_infos
WHERE marketplace_id = {market_id} AND name='{name}'
    AND condition_type='NewItem'
    AND warehouse_condition_code='SELLABLE'
    AND date_period BETWEEN {start_date} AND {end_date}
GROUP BY asin, sku, date_period
ORDER BY asin, sku, date_period;
        '''

        start_date = make_date_period(now - timedelta(days=days))
        end_date = make_date_period(now)

        return fetchall(sql_tmpl.format(market_id=market_id,
                                        name=name,
                                        start_date=start_date,
                                        end_date=end_date))

    @classmethod
    def query_data_at_specific_date(cls, market_id, name, specific_date):
        end_date = specific_date + timedelta(days=1)

        return cls.query_recent_inventory_per_sku(market_id, name,
                                                  now=end_date, days=1)

    @classmethod
    def query_latest_inventory_per_sku(cls, market_id, name):
        sql_tmpl = '''
WITH shipment AS (
    SELECT info.marketplace_id, info.name, item.sku, item.fnsku,
           SUM(item.qty_shipped - item.qty_received) AS inbound_qty
    FROM amz_shipment_items AS item
    LEFT JOIN amz_shipment_infos AS info ON (
        info.marketplace_id=item.marketplace_id
         AND info.name=item.name
         AND info.shipment_id=item.shipment_id)
    WHERE info.shipment_status in (
    'WORKING', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'CHECKED_IN', 'RECEIVING')
         AND info.marketplace_id={market_id}
         AND info.name='{name}'
    GROUP BY info.marketplace_id, info.name, item.sku, item.fnsku
), inv AS(
SELECT inv_infos.marketplace_id, inv_infos.name,
       inv_infos.asin, inv_infos.sku,
       (inv_infos.quantity_available + inv_infos.reserved_qty) AS inventory_qty
FROM amz_fba_inv_infos AS inv_infos
WHERE (inv_infos.sku, inv_infos.date_period) IN (
    SELECT sku, MAX(date_period) FROM amz_fba_inv_infos GROUP BY sku)
    AND condition_type='NewItem' AND warehouse_condition_code='SELLABLE'
)
SELECT inv.marketplace_id, inv.name, inv.asin, inv.sku,
       inv.inventory_qty,
       COALESCE(shipment.inbound_qty, 0) as inbound_qty
FROM inv
FULL OUTER JOIN shipment ON (
    inv.marketplace_id=shipment.marketplace_id
    AND inv.name=shipment.name
    AND inv.sku=shipment.sku
)
        '''
        return fetchall(sql_tmpl.format(market_id=market_id, name=name))

    @classmethod
    def get_by_market_sku_condition(cls, market_id, sku,
                                    cond_type=CT_NEW,
                                    cond_code=WCC_SELLABLE,
                                    date_period=make_date_period()):
        return DBsession.query(cls).filter(
            cls.marketplace_id == market_id,
            cls.sku == sku,
            cls.condition_type == cond_type,
            cls.warehouse_condition_code == cond_code,
            cls.date_period == date_period).first()

    @classmethod
    def save(cls, market_id, name, rep_type, json_data, commit=False):
        if rep_type == AmzReportRequest.RESERVED_SKU:
            json_data['condition_type'] = AmzFbaInvInfo.CT_NEW
            json_data['warehouse_condition_code'] = AmzFbaInvInfo.WCC_SELLABLE

        if rep_type == AmzReportRequest.FBA_INVENTORY:
            json_data['sku'] = json_data.get('seller_sku')

        data = AmzFbaInvInfo.get_by_market_sku_condition(
            market_id, json_data.get('sku'), json_data.get('condition_type'),
            json_data.get('warehouse_condition_code'))

        if not data:
            data = AmzFbaInvInfo(marketplace_id=market_id, name=name)
            AmzReport.convert(cls, data, rep_type, json_data)
            data.add(commit=commit)
            return

        AmzReport.convert(cls, data, rep_type, json_data)
        data.update(commit=commit)



    #-------------------------------
    @classmethod
    def query_latest_fba_inv_info_order_by_nanme_desc(cls):

        Inv_Sku_Date =  DBsession.query(AmzFbaInvInfo.sku, func.max(cls.date_period).label("max_date")).group_by(cls.sku).subquery()#这是一条查询语句
            
        return  DBsession.query(cls.marketplace_id,
                              cls.name,
                              cls.asin,cls.sku,
                              cls.fnsku,
                              cls.quantity_available,
                              cls.reserved_qty,
                              (cls.quantity_available+cls.reserved_qty).label("inventory_qty")#,Inv_Sku_Date,AmzFbaInvInfo.condition_type,AmzFbaInvInfo.warehouse_condition_code
                            ).filter(and_(cls.sku == Inv_Sku_Date.c.sku, 
                                          cls.date_period == Inv_Sku_Date.c.max_date, 
                                          cls.condition_type =="NewItem", 
                                          cls.warehouse_condition_code =="SELLABLE")
                            ).order_by(desc( cls.name)
                            ).all()


class AmzShipmentInfo(Base, BaseMethod):
    __tablename__ = 'amz_shipment_infos'

    SM_WORKING = 'WORKING'
    SM_SHIPPED = 'SHIPPED'
    SM_IN_TRANSIT = 'IN_TRANSIT'
    SM_DELIVERED = 'DELIVERED'
    SM_CHECKED_IN = 'CHECKED_IN'
    SM_RECEIVING = 'RECEIVING'
    SM_CLOSED = 'CLOSED'
    SM_CANCELLED = 'CcancelledANCELLED'
    SM_DELETED = 'DELETED'
    SM_ERROR = 'ERROR'

    _AVAIL_STATUS = [SM_WORKING, SM_SHIPPED, SM_IN_TRANSIT, SM_DELIVERED,
                     SM_CHECKED_IN, SM_RECEIVING]

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, default=1)
    name = Column(VARCHAR(32), nullable=False)
    shipment_id = Column(VARCHAR(16))
    shipment_name = Column(VARCHAR(64))
    shipment_status = Column(VARCHAR(32))
    shipment_label_prep_type = Column(VARCHAR(64), default='SELLER_LABEL')
    shipment_fc = Column(VARCHAR(32))
    working_at = Column(TIMESTAMP(timezone=True))
    shipped_at = Column(TIMESTAMP(timezone=True))
    in_transit_at = Column(TIMESTAMP(timezone=True))
    delivered_at = Column(TIMESTAMP(timezone=True))
    checked_in_at = Column(TIMESTAMP(timezone=True))
    receiving_at = Column(TIMESTAMP(timezone=True))
    closed_at = Column(TIMESTAMP(timezone=True))
    cancelled_at = Column(TIMESTAMP(timezone=True))
    deleted_at = Column(TIMESTAMP(timezone=True))
    error_at = Column(TIMESTAMP(timezone=True))

    @classmethod
    def get_shipment_avail_status(cls):
        return cls._AVAIL_STATUS

    @classmethod
    def get_by_shipment_id(cls, market_id, name, shipment_id):
        return DBsession.query(cls).filter(
            cls.marketplace_id == market_id, cls.name == name,
            cls.shipment_id == shipment_id).first()

    def _update_status(self, status):
        if self.shipment_status == status:
            return

        field_name = '%s_at' % status.strip().lower()
        if not hasattr(self, field_name):
            return

        self.shipment_status = status
        setattr(self, field_name, datetime.now().replace(tzinfo=pytz.UTC))

    @classmethod
    def get_avail_shipment(cls, market_id, name):
        return DBsession.query(cls).filter(
            cls.marketplace_id == market_id, cls.name == name,
            cls.shipment_status.in_(cls.get_shipment_avail_status())).all()

    @classmethod
    def save(cls, market_id, name, shipment_id, shipment_name,
             shipment_status, label_prep_type, shipment_fc,
             commit=False):

        data = AmzShipmentInfo.get_by_shipment_id(market_id, name, shipment_id)
        if not data:
            data = AmzShipmentInfo(marketplace_id=market_id, name=name,
                                   shipment_id=shipment_id,
                                   shipment_name=shipment_name,
                                   shipment_label_prep_type=label_prep_type,
                                   shipment_fc=shipment_fc)
            data._update_status(shipment_status)
            data.add(commit=commit)
            return

        data._update_status(shipment_status)
        data.update(commit=commit)


class AmzShipmentItem(Base, BaseMethod):
    __tablename__ = 'amz_shipment_items'

    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, default=1)
    name = Column(VARCHAR(32), nullable=False)
    shipment_id = Column(VARCHAR(16))
    sku = Column(VARCHAR(32))
    fnsku = Column(VARCHAR(32))
    qty_in_case = Column(BIGINT, default=0)
    qty_shipped = Column(BIGINT, default=0)
    qty_received = Column(BIGINT, default=0)

    @classmethod
    def get_all_by_market_name(cls, market_id, name):
        sql_tmpl = '''
SELECT info.marketplace_id, info.name, info.shipment_id,
    info.shipment_status, item.sku, item.fnsku,
    item.qty_in_case, item.qty_shipped, item.qty_received
FROM amz_shipment_items AS item LEFT JOIN amz_shipment_infos as info ON (
    info.marketplace_id=item.marketplace_id
    AND info.name=item.name
    AND info.shipment_id=item.shipment_id)
WHERE info.marketplace_id = {market_id} AND info.name='{name}'
    AND info.shipment_status in (
    'WORKING', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'CHECKED_IN', 'RECEIVING')
        '''
        return fetchall(sql_tmpl.format(market_id=market_id, name=name))

    @classmethod
    def get_by_shipment_id_sku_fnsku(cls, market_id, name, shipment_id, sku,
                                     fnsku):
        return DBsession.query(cls).filter(
            cls.marketplace_id == market_id, cls.name == name,
            cls.shipment_id == shipment_id, cls.sku == sku,
            cls.fnsku == fnsku).first()

    @classmethod
    def save(cls, market_id, name, shipment_id, sku, fnsku, qty_in_case,
             qty_shipped, qty_received, commit=False):
        data = cls.get_by_shipment_id_sku_fnsku(market_id, name, shipment_id,
                                                sku, fnsku)
        if not data:
            data = AmzShipmentItem(marketplace_id=market_id, name=name,
                                   shipment_id=shipment_id, sku=sku,
                                   fnsku=fnsku, qty_in_case=qty_in_case,
                                   qty_shipped=qty_shipped,
                                   qty_received=qty_received)
            data.add(commit=commit)
            return

        data.qty_shipped = qty_shipped
        data.qty_received = qty_received
        data.update(commit=commit)



#---------------------------------------------------------------------------------------------------
    @classmethod
    def query_shipment_info(cls):
        return  DBsession.query(cls.sku,
                            cls.fnsku,
                            # cls.qty_shipped,
                            # cls.qty_received,
                            func.sum(cls.qty_shipped-cls.qty_received).label("inbound_qty"),
                            AmzShipmentInfo.marketplace_id,
                            AmzShipmentInfo.name
                             ).outerjoin(
                                        AmzShipmentInfo,
                                        and_(AmzShipmentInfo.marketplace_id == cls.marketplace_id,
                                            AmzShipmentInfo.name == cls.name,
                                            AmzShipmentInfo.shipment_id == cls.shipment_id)
                             ).filter(AmzShipmentInfo.shipment_status.in_(("WORKING", "SHIPPED", "IN_TRANSIT", "DELIVERED", "CHECKED_IN", "RECEIVING"))
                             ).group_by(AmzShipmentInfo.marketplace_id,
                                        AmzShipmentInfo.name,
                                        cls.sku,
                                        cls.fnsku,
                                        # cls.qty_shipped,
                                        # cls.qty_received
                             ).all()


class AmzWatchedAsin(Base, BaseMethod):
    __tablename__ = 'amz_watched_asins'

    RULE_KW_RANKING = 0
    RULE_ASIN_BASIC = 1
    RULE_ASIN_BSR = 2
    RULE_ASIN_REVIEW = 3
    RULE_ORDER = 4
    RULE_RETURN = 5  # including return / full refund issued by customer
    RULE_STORAGE = 6

    id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, ForeignKey('amz_account_infos.id'))
    marketplace_id = Column(BIGINT, default=1)
    asin = Column(VARCHAR(16), nullable=False)
    rule_list = Column(BIT(varying=True), default=B'1111111111111111')
    asin_status = Column(Integer)

    @classmethod
    def get_by_market_rule(cls, marketplace_id, rule):
        return DBsession.query(cls).filter(
            cls.marketplace_id == marketplace_id,
            'get_bit(rule_list, %s) != 0' % rule).all()

    @classmethod
    def get_by_market(cls, marketplace_id):
        return DBsession.query(cls).filter(
            cls.marketplace_id == marketplace_id).all()

    @classmethod
    def supported_rules(cls):
        return [cls.RULE_KW_RANKING, cls.RULE_ASIN_BASIC, cls.RULE_ASIN_BSR,
                cls.RULE_ASIN_BSR, cls.RULE_ASIN_REVIEW, cls.RULE_ORDER,
                cls.RULE_RETURN, cls.RULE_STORAGE]

    def has_kw_ranking(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_KW_RANKING)

    def has_asin_basic(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_ASIN_BASIC)

    def has_asin_bsr(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_ASIN_BSR)

    def has_asin_review(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_ASIN_REVIEW)

    def has_order(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_ORDER)

    def has_return(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_RETURN)

    def has_storage(self):
        return int(self.rule_list, 2) & (0x1 << self.RULE_STORAGE)
#-------------------------------------------------------------------
    @classmethod
    def get_by_asin_status():
        return DBsession.query(cls.marketplace_id,cls.asin
                            ).filter(cls.asin_status == 1
                            ).group_by(cls.marketplace_id,cls.asin
                            ).order_by(asc(cls.marketplace_id)
                            ).all()

    @classmethod
    def get_watched_fba_marketplace_id_asin_sku_asc(cls):

        AllFbaIdAsinSku = DBsession.query(AmzMarketplace.id,
                                          AmzSellerOrder.name,
                                          AmzSellerOrder.asin,
                                          AmzSellerOrder.sku,
                                          func.substr(AmzMarketplace.website,12,16).label('marketplaces')
                                          ).join(AmzSellerOrder,
                                                 func.substr(AmzSellerOrder.sales_channel,8,9) == func.substr(AmzMarketplace.website,12,16)
                                          ).filter(AmzSellerOrder.fulfillment_channel != 'Merchant'
                                          ).group_by(AmzMarketplace.id,
                                                     AmzSellerOrder.name,
                                                     AmzSellerOrder.asin,
                                                     AmzSellerOrder.sku,
                                                     func.substr(AmzMarketplace.website,12,16)
                                          ).order_by(asc(AmzMarketplace.id)
                                          ).subquery()
        

        return DBsession.query(cls.marketplace_id,
                               AllFbaIdAsinSku.c.name,
                               cls.asin,
                               AllFbaIdAsinSku.c.sku,
                               AllFbaIdAsinSku.c.marketplaces
                              ).filter(and_(cls.marketplace_id == AllFbaIdAsinSku.c.id,
                                            cls.asin == AllFbaIdAsinSku.c.asin,
                                            cls.marketplace_id.isnot(None),
                                            cls.asin.isnot(None),
                                            AllFbaIdAsinSku.c.sku.isnot(None),
                                            cls.asin_status == 1
                                            )
                              ).group_by(cls.marketplace_id,
                                         AllFbaIdAsinSku.c.name,
                                         cls.asin,
                                         AllFbaIdAsinSku.c.sku,
                                         AllFbaIdAsinSku.c.marketplaces
                              ).order_by(asc(cls.marketplace_id)
                              ).all()






class AmzAsinKwThreshold(Base, BaseMethod):
    __tablename__ = 'amz_asin_kw_threshold'

    id = Column(BIGINT, primary_key=True)
    account_id = Column(BIGINT, ForeignKey('amz_account_infos.id'))
    marketplace_id = Column(BIGINT, default=1)
    asin = Column(VARCHAR(16), nullable=False)
    keywords = Column(VARCHAR(512))
    threshold = Column(BIGINT, default=5)

    @classmethod
    def get_by_market(cls, marketplace_id):
        return DBsession.query(cls).filter(
            cls.marketplace_id == marketplace_id).all()


class AmzAsinLog(BaseMethod):
    id = Column(BIGINT, primary_key=True)
    marketplace_id = Column(BIGINT, nullable=False)
    asin = Column(VARCHAR(64), nullable=False)
    create_date = Column(BIGINT, default=make_date_period)

    @staticmethod
    def get_prev_info(cls, market_id, asin):
        return DBsession.query(cls)\
            .filter(cls.marketplace_id == market_id,
                    cls.asin == asin,
                    cls.create_date != make_date_period())\
            .order_by(cls.create_date.desc()).first()

    @staticmethod
    def get_today_info(cls, market_id, asin):
        return DBsession.query(cls)\
            .filter(cls.marketplace_id == market_id,
                    cls.asin == asin,
                    cls.create_date == make_date_period(),)\
            .all()

    @staticmethod
    def get_asins_today(cls, market_id):
        return DBsession.query(cls)\
            .filter(cls.marketplace_id == market_id,
                    cls.create_date == make_date_period(),)\
            .all()


class AmzAsinInfoLog(Base, AmzAsinLog):
    __tablename__ = 'amz_asin_info_logs'

    title = Column(VARCHAR(512), nullable=False)
    image_cnt = Column(BIGINT, nullable=False)

    @classmethod
    def get_prev_info(cls, market_id, asin):
        return AmzAsinLog.get_prev_info(cls, market_id, asin)

    @classmethod
    def get_asins_today(cls, market_id):
        return AmzAsinLog.get_asins_today(cls, market_id)

    @classmethod
    def save(cls, market_id, asin, title, image_cnt):
        last_asin_info = cls.get_prev_info(market_id=market_id, asin=asin)
        if not last_asin_info or\
            last_asin_info.title != title or\
                last_asin_info.image_cnt != image_cnt:
                AmzAsinInfoLog(marketplace_id=market_id,
                               asin=asin,
                               title=title,
                               image_cnt=image_cnt).add()
#------------------------------------------------------------------------------------------------
    @classmethod
    def get_all_marketpalce_id_asin_order_by_marketplace_id_asc(cls):
        return DBsession.query(cls.marketplace_id,cls.asin
                            ).group_by(cls.marketplace_id,cls.asin
                            ).order_by(asc(cls.marketplace_id)
                            ).all()


class AmzAsinBsrLog(Base, AmzAsinLog):
    __tablename__ = 'amz_asin_bsr_logs'

    seller_ranks = Column(JSONB)

    @classmethod
    def get_prev_info(cls, market_id, asin):
        return AmzAsinLog.get_prev_info(cls, market_id, asin)

    @classmethod
    def get_asins_today(cls, market_id):
        return AmzAsinLog.get_asins_today(cls, market_id)

    @classmethod
    def save(cls, market_id, asin, seller_ranks):
        last_asin_info = cls.get_prev_info(market_id=market_id, asin=asin)
        if not last_asin_info or last_asin_info.seller_ranks != seller_ranks:
            AmzAsinBSRLog(marketplace_id=market_id,
                          asin=asin,
                          seller_ranks=seller_ranks
                          ).add()
#--------------------------------------------------------------------------------------------------------
    @classmethod
    def query_Latest_Bsr_Rank(cls):

        Rank_Markerplaceid_Asin_Date = DBsession.query(cls.marketplace_id,
                                                       cls.asin,
                                                       func.max(cls.create_date).label("create_date")
                                                       ).filter(cls.seller_ranks != '{}'
                                                       ).group_by(cls.marketplace_id,cls.asin
                                                       ).subquery()

        return DBsession.query(cls.id,
                               cls.marketplace_id,
                               cls.asin,
                               cls.seller_ranks,
                               cls.create_date
                              ).filter(and_(cls.marketplace_id == Rank_Markerplaceid_Asin_Date.c.marketplace_id,
                                            cls.asin == Rank_Markerplaceid_Asin_Date.c.asin,
                                              #label("date")不能被用在filter中
                                            cls.create_date == Rank_Markerplaceid_Asin_Date.c.create_date)
                              ).group_by(cls.marketplace_id,cls.asin,cls.seller_ranks,cls.create_date,cls.id
                              ).order_by (asc(cls.id)
                              ).all()



class AmzAsinReviewLog(Base, AmzAsinLog):
    __tablename__ = 'amz_asin_review_logs'

    review_cnt = Column(BIGINT, default=1)
    review_rate = Column(REAL, default=5.0)

    @classmethod
    def get_prev_info(cls, market_id, asin):
        return AmzAsinLog.get_prev_info(cls, market_id, asin)

    @classmethod
    def get_asins_today(cls, market_id):
        return AmzAsinLog.get_asins_today(cls, market_id)

    @classmethod
    def save(cls, market_id, asin, review_cnt, review_rate):
        last_asin_info = cls.get_prev_info(market_id=market_id, asin=asin)
        if not last_asin_info or\
            last_asin_info.review_cnt != review_cnt or\
                last_asin_info.review_rate != review_rate:
                AmzAsinReviewLog(marketplace_id=market_id,
                                 asin=asin,
                                 review_cnt=review_cnt,
                                 review_rate=review_rate).add()
#-------------------------------------------------------------------------------
    @classmethod
    def query_latest_review_cnt(cls):
        Max_Date = DBsession.query(cls.marketplace_id,
                                   cls.asin,
                                   func.max(cls.create_date).label("create_date")
                                  ).group_by(cls.marketplace_id,cls.asin
                                  ).subquery()
        return DBsession.query(cls.marketplace_id,
                               cls.asin,
                               cls.review_cnt,
                               func.max(cls.create_date).label("latest_create_date")
                              ).filter(and_(cls.marketplace_id == Max_Date.c.marketplace_id,
                                            cls.asin == Max_Date.c.asin,
                                            cls.create_date == Max_Date.c.create_date
                                            )
                              ).group_by(cls.marketplace_id,cls.asin,cls.review_cnt
                              ).all()


class AmzAsinReviewDetailLog(Base, AmzAsinLog):
    __tablename__ = 'amz_asin_review_detail_logs'

    review_id = Column(VARCHAR(32), default='')
    title = Column(VARCHAR(256), default='')
    rating = Column(BIGINT, default=0)
    reviewer = Column(VARCHAR(256), default='')
    reviewer_id = Column(VARCHAR(32), default='')
    date_period = Column(BIGINT, default=0)
    is_vp = Column(BOOLEAN, default=False)
    content = Column(TEXT, default='')
    has_image = Column(BOOLEAN, default=False)
    images = Column(JSONB, default='')
    has_video = Column(BOOLEAN, default=False)
    videos = Column(JSONB, default='')

    @classmethod
    def get_prev_info(cls, market_id, asin):
        return AmzAsinLog.get_prev_info(cls, market_id, asin)

    @classmethod
    def get_asins_today(cls, market_id):
        return AmzAsinLog.get_asins_today(cls, market_id)

    @classmethod
    def get_review(cls, market_id, asin, review_id):
        return DBsession.query(cls).filter(cls.marketplace_id == market_id,
                                           cls.asin == asin,
                                           cls.review_id == review_id).first()

    @classmethod
    def save(cls, market_id, asin, review_id, title, rating, reviewer,
             reviewer_id, date_period, is_vp, content, has_image, images,
             has_video, videos, commit=False):
        review = cls.get_review(market_id=market_id, asin=asin,
                                review_id=review_id)
        if not review:
            AmzAsinReviewDetailLog(
                marketplace_id=market_id, asin=asin, review_id=review_id,
                title=title, rating=rating, reviewer=reviewer,
                reviewer_id=reviewer_id, date_period=date_period, is_vp=is_vp,
                content=content, has_image=has_image, images=images,
                has_video=has_video, videos=videos).add(False)

        if commit:
            BaseMethod.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#定义Business_report类
class AmzDailyBusninessReport(Base,BaseMethod):
    
    __tablename__ = 'amz_daily_business_report'

    #表的结构
    id = Column(Integer, primary_key=True)
    marketplace_id =Column(Integer)

    parent_asin = Column(VARCHAR(16))
    child_asin = Column(VARCHAR(16))
    
    title = Column(VARCHAR(512))
    
    sessions = Column(Integer)
    session_percentage = Column(VARCHAR(16))

    page_views = Column(Integer)
    page_views_percentage = Column(VARCHAR(16))
    buy_box_percentage = Column(VARCHAR(16))

    units_ordered = Column(Integer)
    unit_session_percentage = Column(VARCHAR(16))

    ordered_product_sales = Column(Numeric(10,2))
    total_order_items  = Column(Integer)

    report_date = Column(Date)


    @classmethod
    def query_latest_buy_box_percentage(cls):
        Marketplace_Id_Max_Date = DBsession.query(cls.marketplace_id,
                                                  func.max(cls.report_date).label("max_report_date")
                                                 ).group_by(cls.marketplace_id).subquery()

        return DBsession.query(cls).filter(and_(cls.marketplace_id == Marketplace_Id_Max_Date.c.marketplace_id,
                                                cls.report_date == Marketplace_Id_Max_Date.c.max_report_date
                                                )
                                          ).all()

#定义amz_cost_fee_logs类
class AmzCostFeeLog(Base,BaseMethod):

    __tablename__ = 'amz_cost_fee_logs'

    #表的结构
    id = Column(Integer, primary_key=True)
    marketplace_id =Column(Integer)
    product_name = Column(VARCHAR(64))

    asin = Column(VARCHAR(64))
    sku = Column(VARCHAR(32))  

    cost = Column(Numeric(10,2))
    fba_fulfilment_fee_per_unit = Column(Numeric(10,2))
    

    create_date = Column(Date)
        

#定义amz_transaction_infos类
class AmzTransactionInfo(Base,BaseMethod):

    __tablename__ = 'amz_transaction_infos'

    #表的结构
    id = Column(Integer, primary_key=True)
    date_time = Column(TIMESTAMP(timezone=False))
    settlement_id = Column(VARCHAR(32))
    type = Column(VARCHAR(32))
    order_id = Column(VARCHAR(32))
    sku = Column(VARCHAR(64))
    description = Column(VARCHAR(256))
    quantity = Column(BIGINT, default=0)
    marketplace = Column(VARCHAR(32))  
    fulfillment_channel = Column(VARCHAR(32))
    order_city = Column(VARCHAR(256))
    order_state = Column(VARCHAR(256))
    order_postal = Column(VARCHAR(32))
    product_sales = Column(Numeric(10,2))
    shipping_credits = Column(Numeric(10,2))
    gift_wrap_credits = Column(Numeric(10,2))
    promotional_rebates = Column(Numeric(10,2))
    sales_tax_collected = Column(Numeric(10,2))
    selling_fees = Column(Numeric(10,2))
    fba_fees = Column(Numeric(10,2))
    other_transaction_fees = Column(Numeric(10,2))
    other = Column(Numeric(10,2))
    total = Column(Numeric(10,2))

    @classmethod
    def accounting_sku_qty_profit_statistics(cls):
        return DBsession.query(cls.sku,
                               func.sum(cls.quantity).label("quantity"),
                               func.sum(cls.product_sales+
                                        cls.shipping_credits+
                                        cls.gift_wrap_credits+
                                        cls.promotional_rebates+
                                        cls.sales_tax_collected+
                                        cls.selling_fees+
                                        cls.fba_fees+
                                        cls.other_transaction_fees+
                                        cls.other
                                        ).label("total"),
                               func.sum(cls.total).label("profit"),
                               cls.fulfillment_channel,
                               cls.marketplace,
                              ).filter(and_(cls.date_time.between('2017-10-01','2017-11-01'),
                                            cls.type == 'Order',
                                           )
                              ).group_by(cls.fulfillment_channel,
                                         cls.sku,
                                         cls.marketplace,                                         
                              ).order_by(cls.fulfillment_channel,
                                         cls.marketplace,
                                         cls.sku
                              ).all()

    @classmethod
    def accounting_other_expensess_statistics(cls):
        return DBsession.query(cls.type,
                               func.sum(cls.total).label("expenses"),
                               cls.marketplace
                              ).filter(cls.type!="Order"
                              ).group_by(cls.type,cls.marketplace
                              ).order_by(cls.marketplace,cls.type
                              ).all()


  
#-------------------------------------------------------------------------------------------------------------


_managed_table_clz = [ECSPProxyips, ECSPTarget, ECSPProxySpeed,
                      ECSPUserAgent, ECSPPrivateProxy,
                      ECSPPrivateProxySpeed, AmzMarketplace,
                      AmzKeywordsRanking,
                      AmzUserTrackedAsinKeyword, AmzDiagnosedAsinInfo,
                      AmzAsinOffer, AmzMerchantInfo, AmzUserTrackedAsin,
                      AmzBestSeller, AmzBestSellerUrl,
                      AmzAccountInfo, ECSPRealAddress, AmzKwRankImprPrj,
                      AmzKwRankImprDailyPrjLog, AmzKwRankImprDailyAccountLog,
                      AmzKwRankImprDailyDetailLog, AmzUserTrackedAsinStock,
                      ECSPAmzMailTmpl, ECSPAmzMail, EcspRole, EcspUserRole,
                      EcspService, EcspRoleDefaultQuota, EcspUserServiceQuota,
                      EcspUserServiceUsageLog, EcspUserServiceMonthlyQuota,
                      EcspSuperUrlGroup, EcspSuperUrl, EcspClick,
                      EcspArchiveTable,
                      AmzSellerChannel,
                      AmzBestSellerPage,
                      AmzSeoFailureLog, ECSPAmzGroup,
                      AmzAdvertisingAPIAccount,
                      AmzUserPromotion, AmzPromotionCoupon,
                      AmzReviewer, AmzReviewerInfo, EcspReviewer,
                      EcspRefTag,
                      AmzSaleFarmPrj,
                      AmzSaleFarmCoupon,
                      AmzSaleFarmGiftCard,
                      AmzSaleFarmReview,
                      AmzSaleFarmPrjTask,
                      AmzSaleFarmRealAddress,
                      EcspReviewerRole, EcspReviewerScore,
                      EcspUserWechatRelation,
                      AmzUserProfile, AmzKwRankImprPrjLog,
                      AmzReviewerRequestCoupon, AmzFailAccountLog,
                      ECSPAmzWechatTmpl, ECSPAmzServiceChargeLog,
                      AmzAsinVariants, AmzLongTailKeyword,
                      AmzNewSuperurlTestLog,
                      AmzLongTailFailureKeyword,
                      AmzKeywordsNode,
                      AmzKwRankImprPrjParam,
                      AmzAccountCreatedList, AmzAsinInList,
                      AmzAccountListInfo,
                      AmzWatchedAsin, AmzAsinKwThreshold,
                      AmzAsinInfoLog, AmzAsinBsrLog, AmzAsinReviewLog,
                      AmzMWSAccount, AmzReportRequest, AmzFbaInvInfo,
                      AmzSellerOrder, AmzSellerOrderAddress,
                      AmzShipmentInfo, AmzShipmentItem,
                      AmzAsinReviewDetailLog,
                      AmzTransactionInfo]


for c in _managed_table_clz:
    Base.metadata.tables[c.__tablename__].create(bind=engine, checkfirst=True)
#-------------------------------------------------------------------------------------------

if __name__ == '__main__':
    from ipdb import set_trace
    set_trace()

    # params = {'account_id': 1, 'marketplace_id': 1,
    #            'name_on_ui': 'DennyTest',
    #           'list_url': 'http"//www.amazon.com/dksls/akjldfjkls',
    #           'list_type': 0, 'privacy': 0}
    # obj = AmzAccountCreatedList.save(
    #     params['account_id'], params['marketplace_id'], params['name_on_ui'],
    #     params['list_url'], params['list_type'], params['privacy'])
    # ali_ins = AmzAccountListInfo.save(
    #     params['account_id'], params['marketplace_id'], [obj.id])
    # print ali_ins.delete()

    # def _get_ranking(ranks, asin):
    #     rank = ranks.get_asin_ranking(asin)
    #     if not rank:
    #         return 300
    #     return rank.values()[0]

    # market_id = 4
    # asin = 'B01N4EID5B'
    # kw_data_list = AmzKeywordsRanking.query_all_kw_data_per_date(market_id)
    # for data in kw_data_list:
    #     rank = _get_ranking(data, asin)
    #     if rank != 300:
    #         print '%s ==> %s ' % (data.keywords, rank)

    # proxy1 = ECSPPrivateProxy.get_proxy(target='amazon')
    # proxy1 = ECSPPrivateProxy.get_proxy(target='amazon', country='US')
    # proxy1 = ECSPPrivateProxy.get_proxy(target='amazon', country='EU')
    # proxy2 = ECSPPrivateProxy.get_impr_proxy(target='amazon', country='US')
    # proxy2 = ECSPPrivateProxy.get_impr_proxy(target='amazon', country='EU')
    # proxy3 = ECSPPrivateProxy.get_cpc_proxy(target='amazon', country='US')
    # proxy3 = ECSPPrivateProxy.get_cpc_proxy(target='amazon', country='EU')
    # set_trace()
    # ECSPPrivateProxy.delete_unuseful()
    # AmzAccountInfo.bind_ip_to_account(1)
    # EcspRefTag.default_data()
    # AmzPromotionCoupon.query_by_promotion_ids(['1'])
    # EcspService.default_data()
    # all_kw_and_groups = AmzUserTrackedAsinKeyword.get_all_tracked_keywords()
    # from random import shuffle
    # shuffle(all_kw_and_groups)

    # proxy_ips = ['95.211.175.167:13150']
    # for proxy in proxy_ips:
    #     tokens = proxy.split(':')
    #     ECSPPrivateProxy(ip=tokens[0], port=tokens[1], type='https',
    #                      level=1, useful=True,
    #                      havespeed=True, country='US',
    #                      proxy_type=5, is_rotating=True).add(False)

    # BaseMethod.commit()

    # private_proxies = ECSPPrivateProxy.get_all()
    # for proxy in private_proxies:
    #     if proxy.proxy_type != ECSPPrivateProxy.SUN_PROXY:
    #         continue
    #     ECSPPrivateProxySpeed(proxy_id=proxy.id, ip=proxy.ip,
    #                           port=proxy.port,
    #                           type=proxy.type, target='amazon',
    #                           score=5000).add(False)
    # BaseMethod.commit()

    # set_trace()

    # rows = AmzAsinOffer.query_track_asin_offers_by_userid(10)
    # for r in rows:
    #     print r.id, r.market_place_id, r.asin
    #     break

    # EcspReviewerRole.default_data()
    # rows = EcspReviewerScore.query_by_reviewer_ids([1, 3, 4])
    # rows = EcspReviewerScore.query_by_reviewer_ids([2])
    # for row in rows:
    #     print row.id, row.reviewer_role_id, row.reviewer_id, row.score,
    #     print row.cur_requests, row.cur_coupons, row.lasting_bad_reviews

    # print "byebye"
    # EcspRefTag.default_data()
    # AmzPromotionCoupon.query_by_promotion_ids(['1'])
    # EcspService.default_data()

    # ECSPAmzMail.set_read_flag_by_id(3)

    # u = User.get(1)
    # logging.info('==AKE==, u is %s' % u.__dict__)
    # logging.info('u is %s' % u.__dict__)
    # AmzMarketplace.default_data()
    # logging.info('market_places are %s' % AmzMarketplace.get_all())
    # print rank_keywords(1, "('Automotive','Tires')"property, 'lights', 10)

    # ECSPAmzGroup.default_data()
    # keywords_ranking = AmzKeywordsRanking(
    #     market_place_id=1, keywords='hello world')
    # keywords_ranking.add()

    # results1 = {}
    # for i in xrange(1, 10):
    #     results1['A%04x' % i] = i * 10 + 1
    # keywords_ranking.update(results1)

    # keywords_ranking = AmzKeywordsRanking.query_by_keywords_latest(
    #     1, 'hello world')
    # results2 = {}
    # for i in xrange(1, 10):
    #     results2['B%04x' % i] = i * 10 + 2
    # keywords_ranking.update(results2)

    # results3 = {}
    # for i in xrange(1, 10):
    #     results3['C%04x' % i] = i * 10 + 3
    # keywords_ranking.update(results3)

    # AmzUserTrackedAsinKeyword(user_id=1, market_place_id=1,
    #                           asin='B00OCHAS9U',
    #                           keywords='oral b electric toothbrush').add()
    # AmzUserTrackedAsinKeyword(user_id=1, market_place_id=1,
    #                           asin='B00ZISPFHW',
    #                           keywords='oral b electric toothbrush').add()
    # AmzUserTrackedAsinKeyword(user_id=1, market_place_id=1,
    #                           asin='B00OCHAS9U',
    #                           keywords='electric toothbrush').add()

    # keywords = AmzUserTrackedAsinKeyword.query_all_tracked_keywords(1)
    # for kw in keywords:
    #     rankings = AmzKeywordsRanking.query_by_keywords(1, kw)
    #     logging.info('*' * 80)

    #     logging.info('%s, %s' % (kw, len(rankings)))
    #     for ranking in rankings:
    print ('byebye')




