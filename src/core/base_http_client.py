from httpx import Client, HTTPError
from httpx._status_codes import code as status_code

from errors import exceptions


class BaseSyncClient:
    API_REQUEST = "ENDPOINT: {url}. HEADERS: {headers}. PARAMS: {params}. "
    API_NOT_AVALIABLE = f"{API_REQUEST} API not avaliable. ERROR: {{error}}."
    STATUS_CODE_ERROR = f"{API_REQUEST} Unexpected return code: {{status_code}}."

    def __init__(self, headers=None):
        self.sync_client = Client()
        self.headers = headers

    def post(self, url, data, params=None):
        request_params = dict(
            url=url,
            data=data,
            headers=self.headers,
            params=params,
        )
        try:
            response = self.sync_client.post(**request_params)
        except HTTPError as error:
            raise ConnectionError(self.API_NOT_AVALIABLE.format(**request_params, error=error))
        response_status_code = response.status_code
        if response_status_code != status_code.OK:
            raise exceptions.StatusCodeNotOKError(
                self.STATUS_CODE_ERROR.format(**request_params, status_code=response_status_code)
            )
        return response.json()
