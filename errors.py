from requests.exceptions import Timeout
from asyncio import CancelledError, TimeoutError
from aiohttp.client_exceptions import ClientHttpProxyError, ClientProxyConnectionError, ClientOSError


class CaptchaError(Exception):
    pass


ProxyErrors = (CaptchaError, ClientOSError, ClientProxyConnectionError, ClientHttpProxyError)
TimeoutErrors = (Timeout, TimeoutError, CancelledError)
