import tqdm
import asyncio
import async_timeout
import logging.config

from aiohttp import ClientSession
from proxy_mixin import ProxyMixin
from fake_useragent import UserAgent
from base_crawler import BaseCrawler
from settings import ASYNC, LOGGING, PROXY
from utils import io_loop, async_retry, async_detect_captcha, handle_errors, save_to_file, async_control_fitness

SEMAPHORE = ASYNC['semaphore']
TIMEOUT = ASYNC['timeout']
MAX_RETRIES = ASYNC['retries']

USER_AGENT = UserAgent()

logging.config.dictConfig(LOGGING)


class AsyncCrawler(BaseCrawler, ProxyMixin):

    def __init__(self, urls, proxy=False, proxies=None):
        super().__init__(proxies=proxies)
        self._proxy = proxy
        self._urls = urls
        self._session = None
        self._results = None
        self._semaphore = asyncio.Semaphore()
        self._logger = logging.getLogger('async_crawler')
        self._loop = asyncio.get_event_loop()
        self.unreached_urls = list()

    @property
    def session(self):
        if not self._session:
            self._session = ClientSession()
        return self._session

    @property
    def results(self):
        if not self._results:
            self._results = list()
        return self._results

    def pick_proxy(self):
        if self._proxy:
            return super(AsyncCrawler, self).pick_proxy()

    @handle_errors
    @async_detect_captcha
    @async_retry(MAX_RETRIES)
    @async_control_fitness
    async def _fire(self, url, session, proxy):
        """
        Coroutine fires http/https request in an async manner
        :param url: String, url of a website
        :param session: Aiohttp.session, session for firing requests
        :param proxy: String, https proxy
        :return: String, html of a given website
        """
        async with self._semaphore, async_timeout.timeout(TIMEOUT), session.get(url,
                                                                                headers={
                                                                                    'user-agent': USER_AGENT.random},
                                                                                proxy=proxy
                                                                                ) as response:
            return await response.read()

    @io_loop
    async def crawl(self):
        """
        Coroutine crawls a given set of urls
        """
        async with self.session as session:
            coros = tuple(
                asyncio.ensure_future(self._fire(url, session, self.pick_proxy())) for url
                in self._urls)
            for coro in tqdm.tqdm(coros, total=len(coros), ncols=100, desc="Progress"):
                self.results.append(await coro)
            save_to_file(self.unreached_urls)


if __name__ == '__main__':
    # urls = ['http://google.com/'] * 10
    urls = ['http://icanhazip.com/'] * 1
    crawler = AsyncCrawler(urls=urls, proxy=True)
    # print(crawler.proxies)
    crawler.crawl()
    print(crawler.results)
3