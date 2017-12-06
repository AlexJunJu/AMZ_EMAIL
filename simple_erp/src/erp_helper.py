# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys,os
import time
import logging as log
from datetime import datetime, timedelta
from mws_utils import make_mws_api, make_mws_api_by_account
from model import (AmzMWSAccount, AmzReportRequest, AmzSellerOrder, AmzFbaInvInfo, AmzShipmentInfo, AmzShipmentItem,BaseMethod)


#python3使用reload需要from imp import reload
from imp import reload
reload(sys)
#python3 取消了setdefaultencoding
#sys.setdefaultencoding('utf8')

MOCKUP_TEST = False


def do_request_order_report(rep_type, start_date, end_date):

    #遍历亚马逊各站的market_id,name,merchant_id,
    for mws_acct in AmzMWSAccount.get_all():

        #获取亚马逊后台已经生成报表
        obj = AmzReportRequest.get_request(market_id=mws_acct.marketplace_id,
                                           name=mws_acct.name,
                                           rep_type=rep_type,
                                           start_date=start_date,
                                           end_date=end_date)
        #如果已经生成但是没有下载下来
        if obj and not obj.is_done():
            log.warning('AmzReportRequest, <%s, %s, %s, %s, %s, %s>' % (
                mws_acct.marketplace_id, mws_acct.name,
                mws_acct.marketplace_id, rep_type, start_date, end_date))
            continue

        #获取亚马逊后台API
        api = make_mws_api_by_account(mws_acct)
        try:
            req_resp = api.request_report(
                ReportType=rep_type,
                StartDate=start_date, EndDate=end_date)


            #请求获取订单报表
            AmzReportRequest(marketplace_id=mws_acct.marketplace_id,
                             name=mws_acct.name,
                             rep_type=rep_type,
                             request_id=req_resp.RequestReportResult
                                                .ReportRequestInfo
                                                .ReportRequestId,
                             report_id='',
                             start_date=start_date,
                             end_date=end_date,
                             ).add()
        except Exception:
            log.exception('')
            time.sleep(5)


def request_order_report():

    #格式化时间字符串
    def _formate_date(d):
        return d.strftime('%Y-%m-%dT00:00:00Z')

    now = datetime.utcnow()
    start_date = _formate_date(now - timedelta(days=3))
    end_date = _formate_date(now + timedelta(days=1))

    rep_types = AmzSellerOrder.get_report_types()

    #下载报表
    for rep_type in rep_types:
        do_request_order_report(rep_type, start_date, end_date)


#查询报表状态
def check_report():

    #查询正在生成的亚马逊各站(包括marketplace_id,name,rep_type)报表
    ongoing_report_list = AmzReportRequest.find_ongoing_report()

    print('ongoing_report_list:')
    print(ongoing_report_list)

    #定义一个字典类型，进行报表映射
    rep_map = {}
    for rep in ongoing_report_list:
       
        #将marketplace_id、name绑定，作为key键
        key = (rep.marketplace_id, rep.name)

        #如果key键不在字典中，定义一个链表,作为key键的 value值
        if key not in rep_map:
            rep_map[key] = []

        #将rep结果放入列表 rep_map[(rep.marketplace_id, rep.name)]中
        rep_map[key].append(rep)
        #print(rep_map[key])
        #print(rep_map.items())
    

    # for k, v in rep_map.iteritems():   python3 用items()替换iteritems()
    # for k, v in rep_map.items(): 用于遍历字典的（key-value）元组数组
    for k, v in rep_map.items():

        #此处的v应该是rep，如果没有结果跳出本次循环
        if len(v) == 0:
            continue

        market_id, name = k
        #------------------------------------------------------------print(v.marketplace_id,v.name,v.rep_type)
        #print(name)

        #调用亚马逊的接口，通过给定market_id、name
        api = make_mws_api(market_id, name)

        #通过生成器获取request_id
        req_id_list = [data.request_id for data in v]

        # #测试
        # from ipdb import set_trace
        # set_trace()
        # print(req_id_list)

        #调用亚马给定接口
        req_resp = api.get_report_request_list(ReportRequestIdList=req_id_list)
        report_info_list = req_resp.GetReportRequestListResult\
                                   .ReportRequestInfo
        
        # #测试
        print('check_report:-------------------------------------------------------->')
        print(report_info_list)
        
        #如果无结果，跳出本次循环
        if not report_info_list:
            continue

        #用生成器生成一个以ReportRequestId为键，rep为值的键值对
        rep_info_map = {rep.ReportRequestId: rep for rep in report_info_list}
        #将v(即rep)的结果赋值给rep_db_list
        rep_db_list = v

        for rep_db in rep_db_list:

            rep_info = rep_info_map[rep_db.request_id]

            # #测试
            # print(rep_info_map[rep_db.request_id])

            rep_db.status = rep_info.ReportProcessingStatus
            if rep_db.status == AmzReportRequest.ST_DONE:
                rep_db.report_id = rep_info.GeneratedReportId
            #--------------------------------------------------------是不是少了---------------------------------------
            #     # rep.start_date = rep.info.StartDate
            #     # rep.start_date = rep.info.EndDate
            #     rep_db.update(True)
            # else:
                rep_db.update(False)

        BaseMethod.commit()


def do_sync_report_data(report_list, model):
    

    def _get_report(api, report_id):
        while True:
            try:


                # from ipdb import set_trace
                # set_trace()
                #print (type(api.get_report(ReportId=report_id)))
                return api.get_report(ReportId=report_id)
            except Exception as ex:
                for arg in ex.args:
                    if 'hrottled' in arg:
                        log.warning('get_report, RequestThrottled')
                        time.sleep(120)
                        continue
                raise ex
                # if 'hrottled' in ex.message: python3去除了异常类的序列行为和.message属性
                # if 'hrottled' == ex:
                #     log.warning('get_report, RequestThrottled')
                #     time.sleep(120)
                #     continue
                # print(type(ex))
                # raise ex

    for rep in report_list:
        api = make_mws_api(rep.marketplace_id, rep.name)

        print('do_sync_report_data:-------------------------------------------------------->')
        print(rep)
        # print(api)
        # print(rep.report_id)  
        rep_data = _get_report(api, rep.report_id)
       



        # #save data to file
        # with open('./%s_%s.csv' % (rep.rep_type, rep.report_id),'w',encoding='utf-8') as fp:
        #     fp.write(rep_data.decode('utf8','ignore'))
        

        # print(type(rep_data))
        # # rep_data.decode('utf8')
        # print(rep_data.decode('utf8','ignore'))


        #将文本数据分行
        lines = rep_data.decode('utf-8','ignore').split('\r\n')
        header_line = lines[0]
        header = header_line.split('\t')
        header = [token.lower().replace('-', '_').replace(' ', '_').strip()
                  for token in header]
        #for i in xrange(1, len(lines)):python3移除了python2的range,保留了xrange()的实现，并将xrang()重新命名为range()
        for i in range(1, len(lines)):
            data = {}
            line = lines[i].strip()
            if not line:
                continue

            tokens = line.split('\t')
            #for j in xrange(0, len(tokens)):python3移除了python2的range,保留了xrange()的实现，并将xrang()重新命名为range()
            for j in range(0, len(tokens)):
                data[header[j]] = tokens[j].strip()

            model.save(rep.marketplace_id, rep.name, rep.rep_type, data,
                       commit=False)

        rep.downloaded(commit=False)
        BaseMethod.commit()


def download_report():
    

    ready_report_list = AmzReportRequest.find_ready_report()

    def _download_inventory():
        inv_requests = [rep for rep in ready_report_list
                        if rep.rep_type in AmzFbaInvInfo.get_report_types()]
        try:
           do_sync_report_data(inv_requests, AmzFbaInvInfo)
        except Exception:
            log.exception('')

    def _download_order():
        
        

        all_orders = [rep for rep in ready_report_list
                      if rep.rep_type == AmzReportRequest.ALL_ORDER]
        fba_fbm_orders = [rep for rep in ready_report_list
                          if rep.rep_type in [AmzReportRequest.FBA_ORDER,
                                              AmzReportRequest.FBM_ORDER]]
        try:
            do_sync_report_data(all_orders, AmzSellerOrder)
            do_sync_report_data(fba_fbm_orders, AmzSellerOrder)
        except Exception:
            log.exception('')



    # from ipdb import set_trace
    # set_trace()
    _download_inventory()
    _download_order()



#请求获取FBA库存报表
def request_fba_inventory_report():

    #获取库存报表类型，返回的是[AmzReportRequest.FBA_INVENTORY, AmzReportRequest.RESERVED_SKU]
    #即：['_GET_AFN_INVENTORY_DATA_', '_GET_RESERVED_INVENTORY_DATA_']
    rep_types = AmzFbaInvInfo.get_report_types()
    #print(rep_types)

    #获取亚马逊各站的所有信息，调用亚马逊给的接口，通过给定的类型（_GET_AFN_INVENTORY_DATA_、_GET_RESERVED_INVENTORY_DATA_）获取相应的报表
    for mws_acct in AmzMWSAccount.get_all():
    #print(mws_acct.marketplace_id,mws_acct.name,mws_acct.merchant_id)
    



        # #测试
        # from ipdb import set_trace
        # set_trace()

        #调用亚马逊各站的接口，通过给定各站的信息
        api = make_mws_api_by_account(mws_acct)
        for rep_type in rep_types:
            try:

                req_resp = api.request_report(ReportType=rep_type)

                #调用基类Class BaseMethod的add()方法，插入数据库？？？？
                #AmzReportRequest(base)
                AmzReportRequest(marketplace_id=mws_acct.marketplace_id,
                                 name=mws_acct.name,
                                 rep_type=rep_type,
                                 request_id=req_resp.RequestReportResult
                                                    .ReportRequestInfo
                                                    .ReportRequestId,
                                 report_id='',
                                 ).add()
                #测试
                print('request_fba_inventory_report-------------------------------------------------------------------------------->')
                print(mws_acct.marketplace_id,mws_acct.name,rep_type,req_resp.RequestReportResult
                                                    .ReportRequestInfo
                                                    .ReportRequestId)


            except Exception:
                log.exception('')
                time.sleep(5)


def fetch_shipment_data():

    def _list_ib_shipment_items(api, shipment_id):
        while True:
            try:
                return api.list_inbound_shipment_items(ShipmentId=shipment_id)


            except Exception as ex:
                 for arg in ex.args:
                    if 'hrottled' in arg:
                        log.warning('get_report, RequestThrottled')
                        time.sleep(120)
                        continue
            raise ex
                # #python3去除了异常类的序列和.message属性
                # if 'hrottled' in ex.message:
                #     log.warning('list_ib_shipment_items, RequestThrottled')
                #     time.sleep(120)
                #     continue
                # raise ex

    #获取shipment的各种状态
    status_list = AmzShipmentInfo.get_shipment_avail_status()

    def _save_available_shipments(shipment_list):
        for data in shipment_list:
            AmzShipmentInfo.save(
                market_id=mws_acct.marketplace_id,
                name=mws_acct.name,
                shipment_id=data.ShipmentId,
                shipment_name=data.ShipmentName,
                shipment_status=data.ShipmentStatus,
                label_prep_type=data.LabelPrepType,
                shipment_fc=data.DestinationFulfillmentCenterId,
                commit=False)
           #resp1 = _list_ib_shipment_items(api, ShipmentId=data.ShipmentId)
            resp1 = _list_ib_shipment_items(api, data.ShipmentId)
            items = resp1.ListInboundShipmentItemsResult.ItemData
            for item in items:
                AmzShipmentItem.save(market_id=mws_acct.marketplace_id,
                                     name=mws_acct.name,
                                     shipment_id=item.ShipmentId,
                                     sku=item.SellerSKU,
                                     fnsku=item.FulfillmentNetworkSKU,
                                     qty_in_case=item.QuantityInCase,
                                     qty_shipped=item.QuantityShipped,
                                     qty_received=item.QuantityReceived,
                                     commit=False)
            BaseMethod.commit()

    def _get_closed_shipments(market_id, name, shipment_list):
        avail_ids = [sm.ShipmentId for sm in shipment_list]
        shipment_list_db = AmzShipmentInfo.get_avail_shipment(market_id, name)
        return [sm.shipment_id for sm in shipment_list_db
                if sm.shipment_id not in avail_ids]

    for mws_acct in AmzMWSAccount.get_all():
        api = make_mws_api_by_account(mws_acct)
        resp = api.list_inbound_shipments(ShipmentStatusList=status_list)
        shipment_list = resp.ListInboundShipmentsResult.ShipmentData
        _save_available_shipments(shipment_list)

        closed_ids = _get_closed_shipments(mws_acct.marketplace_id,
                                           mws_acct.name,
                                           shipment_list)
        if not closed_ids:
            continue
        resp = api.list_inbound_shipments(ShipmentIdList=closed_ids)
        shipment_list = resp.ListInboundShipmentsResult.ShipmentData
        _save_available_shipments(shipment_list)


if __name__ == '__main__':

    #第三方库ipdb,用以调试python，在程序需要中断的地方插入以下两句就可以
    #运行程序后，在执行到set_trace()的时候中断程序，并出现提示符（ipdb）……
    # from ipdb import set_trace
    # set_trace()

    #加载日志文件logging，通过logging.basicConfig函数如日志格式及方式做相关配置
    import logging as log
    log.basicConfig(level=log.INFO)

    MOCKUP_TEST = False

    # check_list_clz = [CheckAsinKwRanking]

    # from utils import get_page_source_cookies
    # from urllib import urlencode

    # target = 'https://hooks.pubu.im/services/w999128ep13qt6x'
    # data = {'text': 'Hello world 123'}
    # get_page_source_cookies(target=target, data=urlencode(data))

    # def _import_data(start_date, end_date):
    #     rep_types = AmzSellerOrder.get_order_report_types()
    #     for rep_type in rep_types:
    #         do_request_order_report(rep_type, start_date, end_date)

    #     # request_order_report()
    #     # time.sleep(20 * 60)
    #     # check_order_report()
    #     # download_order_report()
    #     # time.sleep(10)

    # periods = [
    #     # {'start': '2016-08-01T00:00:00Z', 'end': '2016-08-31T23:59:59Z'},
    #     # {'start': '2016-09-01T00:00:00Z', 'end': '2016-09-30T23:59:59Z'},
    #     # {'start': '2016-10-01T00:00:00Z', 'end': '2016-10-31T23:59:59Z'},
    #     # {'start': '2016-11-01T00:00:00Z', 'end': '2016-11-30T23:59:59Z'},
    #     # {'start': '2016-12-01T00:00:00Z', 'end': '2016-12-31T23:59:59Z'},
    #     # {'start': '2017-01-01T00:00:00Z', 'end': '2017-01-31T23:59:59Z'},
    #     {'start': '2017-02-01T00:00:00Z', 'end': '2017-02-28T23:59:59Z'},
    #     # {'start': '2017-03-01T00:00:00Z', 'end': '2017-03-31T23:59:59Z'},
    #     # {'start': '2017-04-01T00:00:00Z', 'end': '2017-04-30T23:59:59Z'},
    #     # {'start': '2017-05-01T00:00:00Z', 'end': '2017-05-12T23:59:59Z'},
    #     ]
    # for period in periods:
    #     try:
    #         start = period['start']
    #         end = period['end']
    #         log.info('=======%s, %s, starts======' % (start, end))
    #         _import_data(start, end)
    #         log.info('=======%s, %s, ends======' % (start, end))
    #     except Exception:
    #         log.exception('=======%s, %s, ends======' % (start, end))
    #         break

    # all_req_list = AmzReportRequest.get_all()

    # def _filter(req, market_id, name, rep_type, status):
    #     return req.marketplace_id == market_id\
    #            and req.name == name\
    #            and req.rep_type == rep_type\
    #            and req.status == status

    # kl_de_req_list = [req for req in all_req_list
    #                   if _filter(req, 4, 'KingLove',
    #                              AmzReportRequest.FBM_ORDER,
    #                              AmzReportRequest.ST_DOWNLOADED)]
    # do_sync_report_data(kl_de_req_list, AmzSellerOrder)

    # all_req_list = AmzReportRequest.get_all()
    # req_list = [req for req in all_req_list
    #             if req.status == AmzReportRequest.ST_DOWNLOADED]
    # do_sync_report_data(req_list, AmzSellerOrder)



    request_fba_inventory_report()
    check_report()
    download_report()
    fetch_shipment_data()
    print("byebye")
    os._exit(0)
