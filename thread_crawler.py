import requests
import logging.config

from proxy_mixin import ProxyMixin
from fake_useragent import UserAgent
from base_crawler import BaseCrawler
from settings import LOGGING, PROXY, THREAD
from multiprocessing.dummy import Pool as ThreadPool
from utils import retry, detect_captcha, handle_errors, control_fitness


WORKERS = THREAD['workers']
TIMEOUT = THREAD['timeout']
MAX_RETRIES = THREAD['retries']

USER_AGENT = UserAgent()

logging.config.dictConfig(LOGGING)


class ThreadCrawler(BaseCrawler, ProxyMixin):

    def __init__(self, urls, proxy=False, proxies=None):
        super(ThreadCrawler, self).__init__(proxies=proxies)
        self._proxy = proxy
        self._urls = urls
        self._session = None
        self._results = None
        self._thread_pool = None
        self._results = None
        self._logger = logging.getLogger('thread_crawler')
        self.unreached_urls = list()

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        return self._session

    @property
    def thread_pool(self):
        if not self._thread_pool:
            self._thread_pool = ThreadPool(WORKERS)
        return self._thread_pool

    def pick_proxy(self):
        if self._proxy:
            return super().pick_proxy()

    @handle_errors
    @detect_captcha
    @retry(MAX_RETRIES)
    @control_fitness
    def _fire(self, url, session, proxy):
        """
        Method fires http/https request and returns html of a given website
        :param url: String, url
        :param session: requests.session
        :param proxy: String, address of a proxy
        :return: String, html of a given website
        """
        return session.get(url, proxies={'http': proxy}, timeout=TIMEOUT).text

    def crawl(self):
        """
        Method crawls a given set of urls
        """
        with self.thread_pool as pool:
            args = ((url, self.session, self.pick_proxy()) for url in self._urls)
            self._results = pool.starmap(self._fire, args)
            print(self._results)


if __name__ == '__main__':
    # urls = ['https://google.com'] * 1
    urls = ['http://icanhazip.com/'] * 1
    c = ThreadCrawler(urls, proxy=True)
    c.crawl()
