# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys,os
import time
import logging as log
from datetime import datetime, timedelta
from mws_utils import make_mws_api, make_mws_api_by_account
from model import (AmzMWSAccount, AmzReportRequest, AmzSellerOrder, AmzFbaInvInfo, AmzShipmentInfo, AmzShipmentItem,AmzWatchedAsin,BaseMethod)
from imp import reload
reload(sys)

MOCKUP_TEST = False
def do_request_order_report(rep_type, start_date, end_date):
    
    for mws_acct in AmzMWSAccount.get_by_account_status():
        obj = AmzReportRequest.get_request(market_id=mws_acct.marketplace_id,
                                           name=mws_acct.name,
                                           rep_type=rep_type,
                                           start_date=start_date,
                                           end_date=end_date)

        if obj and not obj.is_done():
            log.warning('AmzReportRequest, <%s, %s, %s, %s, %s, %s>' % (
                mws_acct.marketplace_id, mws_acct.name,
                mws_acct.marketplace_id, rep_type, start_date, end_date))
            continue

        api = make_mws_api_by_account(mws_acct)
        try:
            req_resp = api.request_report(ReportType=rep_type,
                                          StartDate=start_date, 
                                          EndDate=end_date)
          
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

    # strftime stringfy tuple of datime
    def _formate_date(d):
        return d.strftime('%Y-%m-%dT00:00:00Z')

    # datetime.now() is local datetime
    # datetime.utcnow() is world time,that is,GMT
    # type of datetime.utcnow() is tuple 
    now = datetime.utcnow()
    # satrt_time,end_time set the time interval during which the report is
    start_date = _formate_date(now - timedelta(days=5))
    end_date = _formate_date(now + timedelta(days=1))
    rep_types = AmzSellerOrder.get_report_types()
    #request report according type of report and datetime interval
    for rep_type in rep_types:
        do_request_order_report(rep_type, start_date, end_date)


def check_report():
    #get ongoning report requests which is _SUBMITTED_ and  _IN_PROGRESS_
    ongoing_report_list = AmzReportRequest.find_ongoing_report()
    rep_map = {}
    for rep in ongoing_report_list:
        #bound (marketplace_id,name) as key
        key = (rep.marketplace_id, rep.name)
        #if the key is not in dict,define a list as the value of key
        if key not in rep_map:
            rep_map[key] = []
        #append the record of rep into  rep_map[(rep.marketplace_id, rep.name)]
        #rep includes marketplace_id,name,rep_type,request_id,report_id,start_date,end_date,status,create_at
        rep_map[key].append(rep)

    # for k, v in rep_map.iteritems():   python3 用items()替换iteritems()
    # for k, v in rep_map.items(): 用于遍历字典的（key-value）元组数组
    for k, v in rep_map.items():
        if len(v) == 0:
            continue
        market_id, name = k
        #get the api by offering market_id、name
        api = make_mws_api(market_id, name)
        #get list of alerdy generated request_id by generator
        req_id_list = [data.request_id for data in v]
        req_resp = api.get_report_request_list(ReportRequestIdList=req_id_list)
        report_info_list = req_resp.GetReportRequestListResult\
                                   .ReportRequestInfo
        #just for test
        print('check_report:-------------------------------------------------------->')
        print(report_info_list)
        
        if not report_info_list:
            continue
        #create a generator ReportRequestId as key，rep as value
        rep_info_map = {rep.ReportRequestId: rep for rep in report_info_list}
        #将v(即rep)的结果赋值给rep_db_list
        rep_db_list = v
        for rep_db in rep_db_list:
            rep_info = rep_info_map[rep_db.request_id]
            rep_db.status = rep_info.ReportProcessingStatus
            if rep_db.status == AmzReportRequest.ST_DONE:
                rep_db.report_id = rep_info.GeneratedReportId
                rep_db.update(False)

        BaseMethod.commit()


def do_sync_report_data(report_list, model):
    
    def _get_report(api, report_id):
        while True:
            try:
                return api.get_report(ReportId=report_id)
            except Exception as ex:
                for arg in ex.args:
                    if 'hrottled' in arg:
                        log.warning('get_report, RequestThrottled')
                        time.sleep(120)
                        continue
                raise ex

    for rep in report_list:
        api = make_mws_api(rep.marketplace_id, rep.name)
        rep_data = _get_report(api, rep.report_id)
        
        # process the text
        lines = rep_data.decode('utf-8','ignore').split('\r\n')
        # process the headrer of text
        header_line = lines[0]
        header = header_line.split('\t')
        header = [token.lower().replace('-', '_').replace(' ', '_').strip()
                  for token in header]

        for i in range(1, len(lines)):
            data = {}
            line = lines[i].strip()
            if not line:
                continue
            tokens = line.split('\t')
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



#request FBA sellable invenrory and reserved inventory
def request_fba_inventory_report():
    #type returned [AmzReportRequest.FBA_INVENTORY, AmzReportRequest.RESERVED_SKU]
    #that is,['_GET_AFN_INVENTORY_DATA_', '_GET_RESERVED_INVENTORY_DATA_']
    rep_types = AmzFbaInvInfo.get_report_types()

    #get all infomation of amazon shops states，that is,marketplace_id name merchant_id key secret
    #get corresponding report thorough api of amz by offering given type（_GET_AFN_INVENTORY_DATA_、_GET_RESERVED_INVENTORY_DATA_）
    for mws_acct in AmzMWSAccount.get_by_account_status():
        # create api by offering information of shop state
        api = make_mws_api_by_account(mws_acct)
        for rep_type in rep_types:
            try:
                req_resp = api.request_report(ReportType=rep_type)
                AmzReportRequest(marketplace_id=mws_acct.marketplace_id,
                                 name=mws_acct.name,
                                 rep_type=rep_type,
                                 request_id=req_resp.RequestReportResult
                                                    .ReportRequestInfo
                                                    .ReportRequestId,
                                 report_id='',
                                 ).add()
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

    status_list = AmzShipmentInfo.get_shipment_avail_status()
    for mws_acct in AmzMWSAccount.get_by_account_status():
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

def append_new_asin():
    new_asin_list = AmzWatchedAsin.get_not_watched_asin()
    if len(new_asin_list)>0 :
        i = 1
        for marketplace_asin in new_asin_list:
            amz_watched_asin = AmzWatchedAsin()
            amz_watched_asin.account_id = 13
            amz_watched_asin.marketplace_id = marketplace_asin.id
            amz_watched_asin.asin = marketplace_asin.asin
            amz_watched_asin.rule_list = '1111111111111111'
            amz_watched_asin.asin_status = 1
            amz_watched_asin.add(False)
            print('adding the %d th asin ' % i,amz_watched_asin.id, amz_watched_asin.asin)
            i=i+1
        try:
            BaseMethod.commit()
        except Exception as ex:
            raise ex
    else:
        pass

def erp_helper():
    import logging as log
    log.basicConfig(level=log.INFO)
    MOCKUP_TEST = False
    request_order_report()
    request_fba_inventory_report()
    check_report()
    download_report()
    fetch_shipment_data()
    append_new_asin()
    print("erp_helper alerdy done its job")

if __name__ == '__main__':

    #第三方库ipdb,用以调试python，在程序需要中断的地方插入以下两句就可以
    #运行程序后，在执行到set_trace()的时候中断程序，并出现提示符（ipdb）……
    # from ipdb import set_trace
    # set_trace()

    #加载日志文件logging，通过logging.basicConfig函数如日志格式及方式做相关配置
    import logging as log
    log.basicConfig(level=log.INFO)

    MOCKUP_TEST = False
    request_order_report()
    request_fba_inventory_report()
    check_report()
    download_report()
    fetch_shipment_data()
    append_new_asin()
    print("byebye")
    os._exit(0)
