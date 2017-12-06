from __future__ import absolute_import

from boto.mws.connection import MWSConnection
import logging as log


def _get_mws_info(key):
    _ALL_MARKET_PLACES = [
        {'id': 1, 'market': 'us', 'marketplace_id': 'ATVPDKIKX0DER',
         'endpoint': 'mws.amazonservices.com'},
        {'id': 3, 'market': 'uk', 'marketplace_id': 'A1F83G8C2ARO7P',
         'endpoint': 'mws-eu.amazonservices.com'},
        {'id': 4, 'market': 'de', 'marketplace_id': 'A1PA6795UKMFR9',
         'endpoint': 'mws-eu.amazonservices.com'},
        {'id': 5, 'market': 'fr', 'marketplace_id': 'A13V1IB3VIYZZH',
         'endpoint': 'mws-eu.amazonservices.com'},
        {'id': 6, 'market': 'jp', 'marketplace_id': 'A1VC38T7YXB528',
         'endpoint': 'mws.amazonservices.jp'},
        {'id': 7, 'market': 'ca', 'marketplace_id': 'A1AM78C64UM0Y8',
         'endpoint': 'mws.amazonservices.com'},
        {'id': 44551, 'market': 'es', 'marketplace_id': 'A1RKKUPIHCS9HS',
         'endpoint': 'mws-eu.amazonservices.com'},
        {'id': 35691, 'market': 'it', 'marketplace_id': 'APJ6JRA9NG5V4',
         'endpoint': 'mws-eu.amazonservices.com'},
        ]

    def _do(market_id):
        for d in _ALL_MARKET_PLACES:
            if d['id'] == market_id:
                return d[key]
        return None

    return _do


mws_get_marketplace_id = _get_mws_info('marketplace_id')
mws_get_endpoint = _get_mws_info('endpoint')


class MWSAPI(MWSConnection):

    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 market_id, merchant_id):
        super(MWSAPI, self).__init__(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            host=mws_get_endpoint(market_id),
            Merchant=merchant_id)
        self.Merchant = merchant_id
        self.SellerId = merchant_id
        self.market_id = mws_get_marketplace_id(market_id)

    def query_orders(self, created_at, created_before=None):
        kw = {'MarketplaceId': [self.market_id], 'CreatedAfter': created_at}
        if not created_before:
            kw['CreatedBefore'] = created_before

        response = self.list_orders(**kw)
        return response.ListOrdersResult.Orders.Order

    def query_order_items(self, created_at, created_before=None):
        orders = self.query_orders(created_at, created_before)
        for order in orders:
            resp = self.list_order_items(AmazonOrderId=order.AmazonOrderId)
            items = resp.ListOrderItemsResult.OrderItems.OrderItem
            for item in items:
                order[item.SellerSKU] = item

        return orders


def make_mws_api_by_account(account):
    return MWSAPI(account.key, account.secret, account.marketplace_id,
                  account.merchant_id)


def make_mws_api(market_id, name):
    from model import AmzMWSAccount

    account = AmzMWSAccount.get_by_market_name(market_id, name)
    if not account:
        return None

    return make_mws_api_by_account(account)


if __name__ == '__main__':
    from ipdb import set_trace
    set_trace()

    import logging as log
    log.basicConfig(level=log.INFO)

    api = make_mws_api(4, 'KingLove')

    # orders = api.query_order_items(created_at='2017-05-03T00:00:00Z',
    #                                created_before='2017-05-09T00:00:00Z')
    # set_trace()
    # for order in orders:
    #     log.info('=' * 80)
    #     log.info('%s, %s, %s, %s, %s, %s, %s, %s' % (
    #         order.PurchaseDate,
    #         order.AmazonOrderId,
    #         order.OrderStatus,
    #         order.FulfillmentChannel,
    #         order.PaymentMethodDetail,
    #         order.OrderTotal,
    #         order.BuyerName if hasattr(order, 'BuyerName') else 'N/A',
    #         order.BuyerEmail if hasattr(order, 'BuyerEmail') else 'N/A'))
    #     for sku, item in order.iteritems():
    #         log.info('\t- %s x %s, %s, %s, %s' % (item.QuantityOrdered,
    #                                               item.ASIN,
    #                                               sku,
    #                                               item.ItemPrice,
    #                                               item.PromotionDiscount))

    # api.manage_report_schedule(ReportType='_GET_FLAT_FILE_ORDERS_DATA_',
    #                            Schedule='_1_HOUR_')

    # while True:
    # req_resp = api.request_report(ReportType='_GET_FLAT_FILE_ORDERS_DATA_',
    #                               StartDate='2017-05-03T00:00:00Z',
    #                               EndDate='2017-05-10T00:00:00Z')

    # def _download_report_2(req_id_list):
    #     rep_resp = api.get_report_list(ReportRequestIdList=req_id_list)
    #     rep_list = rep_resp.GetReportListResult.ReportInfo
    #     for i in xrange(0, len(rep_list)):
    #         report = rep_list[i]
    #         rep_data = api.get_report(ReportId=report.ReportId)
    #         with open('report_%s.csv' % report.ReportId, 'w+') as fp:
    #             fp.write(rep_data)

    # def _download_report():
    #     rep_resp = api.get_report_list(
    #         ReportTypeList=['_GET_FLAT_FILE_ORDERS_DATA_'],
    #         ReportProcessingStatusList=['_DONE_'])
    #     rep_list = rep_resp.GetReportListResult.ReportInfo
    #     for i in xrange(0, len(rep_list)):
    #         report = rep_list[i]
    #         rep_data = api.get_report(ReportId=report.ReportId)
    #         with open('report_%s.csv' % report.ReportId, 'w+') as fp:
    #             fp.write(rep_data)

    # _download_report()
    # _download_report_2([req_resp.RequestReportResult
    #                     .ReportRequestInfo.ReportRequestId])

    status_list = ['WORKING', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED',
                   'CHECKED_IN', 'RECEIVING']
    resp = api.list_inbound_shipments(ShipmentStatusList=status_list)
    shipment_list = resp.ListInboundShipmentsResult.ShipmentData

    msg_tmpl = 'sku:%s, fnsku:%s, qty_in_case:%s, shipped:%s, received:%s'
    for data in shipment_list:
        print('=' * 40)
        print('%s, %s, %s, %s, %s' % (
                data.ShipmentId, data.ShipmentName, data.ShipmentStatus,
                data.LabelPrepType, data.DestinationFulfillmentCenterId
                                    )
            )
        resp1 = api.list_inbound_shipment_items(ShipmentId=data.ShipmentId)
        items = resp1.ListInboundShipmentItemsResult.ItemData
        for item in items:
            print( msg_tmpl % (item.SellerSKU, item.FulfillmentNetworkSKU,
                              item.QuantityInCase, item.QuantityShipped,
                              item.QuantityReceived)
                )

    log.info('byebye')
