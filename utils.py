import asyncio

from functools import wraps
from settings import UNREACHED_URLS_PATH
from errors import CaptchaError, ProxyErrors, TimeoutErrors


def io_loop(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        self._loop.run_until_complete(func(self, *args, **kwargs))
        self._loop.close()
    return inner


def retry(max_retries):
    def wrapper(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def inner(self, url, session, proxy):
                count = 0
                while count < max_retries:
                    try:
                        return await func(self, url, session, proxy)
                    except TimeoutErrors:
                        count += 1
                        if count == max_retries:
                            self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in timeout')
                            self.unreached_urls.append(url)
        else:
            @wraps(func)
            def inner(self, url, session, proxy):
                count = 0
                while count < max_retries:
                    try:
                        return func(self, url, session, proxy)
                    except TimeoutErrors:
                        count += 1
                        if count == max_retries:
                            self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in timeout')
                            self.unreached_urls.append(url)
        return inner
    return wrapper


def _detect_captcha(html):
    pass


def detect_captcha(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(self, url, session, proxy):
            try:
                html = await func(self, url, session, proxy)
                _detect_captcha(html)
            except CaptchaError as e:
                self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in captcha')
                self._logger.warn(f'Removing proxy: {proxy}')
                self.remove_proxy(proxy)
                self.unreached_urls.append(url)
            else:
                return html
    else:
        @wraps(func)
        def wrapper(self, url, session, proxy):
            try:
                html = func(self, url, session, proxy)
                _detect_captcha(html)
            except CaptchaError as e:
                self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in captcha')
                self._logger.warn(f'Removing proxy: {proxy}')
                self.remove_proxy(proxy)
                self.unreached_urls.append(url)
            else:
                return html
    return wrapper


def handle_errors(func):
    if asyncio.iscoroutinefunction(func):
        async def wrapper(self, url, session, proxy):
            try:
                return await func(self, url, session, proxy)
            except Exception as e:
                self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in error: {e}')
                self.unreached_urls.append(url)
    else:
        def wrapper(self, url, session, proxy):
            try:
                return func(self, url, session, proxy)
            except Exception as e:
                self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in error: {e}')
                self.unreached_urls.append(url)
    return wrapper


def save_to_file(ls):
    with open(UNREACHED_URLS_PATH, 'w') as f:
        f.writelines('\n'.join(ls))
