from core.api_gateaway_urls import API_GATEAWAY_URL
from core.base_http_client import BaseSyncClient


class OrderClient(BaseSyncClient):

    def post_order(self, data):
        request_params = dict(url=API_GATEAWAY_URL, data=data)
        return self.post(**request_params)


order_client = OrderClient()
