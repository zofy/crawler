import asyncio

from functools import wraps
from contextlib import contextmanager
from settings import UNREACHED_URLS_PATH
from errors import CaptchaError, TimeoutErrors


def io_loop(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        self._loop.run_until_complete(func(self, *args, **kwargs))
        self._loop.close()
    return inner


@contextmanager
def _handle_errors(self, url, proxy):
    try:
        yield
    except Exception as e:
        self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in error: {e}')
        self.unreached_urls.append(url)


def handle_errors(func):
    @wraps(func)
    def wrapper(self, url, session, proxy):
        if asyncio.iscoroutinefunction(func):
            async def tmp():
                with _handle_errors(self, url, proxy):
                    return await func(self, url, session, proxy)
            return tmp()
        with _handle_errors(self, url, proxy):
            return func(self, url, session, proxy)
    return wrapper


def async_retry(max_retries):
    def wrapper(func):
        @wraps(func)
        async def inner(self, url, session, proxy):
            for _ in range(max_retries):
                try:
                    return await func(self, url, session, proxy)
                except TimeoutErrors:
                    self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in timeout')
                    proxy = self.pick_proxy()
            self.unreached_urls.append(url)
        return inner
    return wrapper


def retry(max_retries):
    def wrapper(func):
        @wraps(func)
        def inner(self, url, session, proxy):
            for _ in range(max_retries):
                try:
                    return func(self, url, session, proxy)
                except TimeoutErrors:
                    self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in timeout')
                    proxy = self.pick_proxy()
            self.unreached_urls.append(url)
        return inner
    return wrapper


def _detect_captcha(html):
    pass


def async_detect_captcha(func):
    @wraps(func)
    async def wrapper(self, url, session, proxy):
        try:
            html = await func(self, url, session, proxy)
            _detect_captcha(html)
        except CaptchaError:
            self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in captcha')
            self._logger.warn(f'Removing proxy: {proxy}')
            self.unreached_urls.append(url)
        else:
            return html
    return wrapper


def detect_captcha(func):
    @wraps(func)
    def wrapper(self, url, session, proxy):
        try:
            html = func(self, url, session, proxy)
            _detect_captcha(html)
        except CaptchaError:
            self._logger.error(f'Reaching url: {url} via proxy: {proxy} resulted in captcha')
            self._logger.warn(f'Removing proxy: {proxy}')
            self.unreached_urls.append(url)
        else:
            return html
    return wrapper


def async_control_fitness(func):
    @wraps(func)
    async def wrapper(self, url, session, proxy):
        try:
            result = await func(self, url, session, proxy)
        except Exception:
            self._logger.warn(f'Decreasing fitness of proxy: {proxy}')
            self._decrease_fitness(proxy)
            raise
        else:
            self._logger.warn(f'Increasing fitness of proxy: {proxy}')
            self._increase_fitness(proxy)
            return result
    return wrapper


def control_fitness(func):
    @wraps(func)
    def wrapper(self, url, session, proxy):
        try:
            result = func(self, url, session, proxy)
        except Exception:
            self._logger.warn(f'Decreasing fitness of proxy: {proxy}')
            self._decrease_fitness(proxy)
            raise
        else:
            self._logger.warn(f'Increasing fitness of proxy: {proxy}')
            self._increase_fitness(proxy)
            return result
    return wrapper


def save_to_file(ls):
    with open(UNREACHED_URLS_PATH, 'w') as f:
        f.writelines('\n'.join(ls))
