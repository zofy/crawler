import logging.config

from random import random
from bisect import bisect_left
from settings import LOGGING, PROXY

logging.config.dictConfig(LOGGING)

PROXY_IPs = PROXY['IPs']
DEFAULT_FITNESS = PROXY['default_fitness']
MIN_FITNESS = PROXY['min_fitness']
MAX_FITNESS = PROXY['max_fitness']


class ProxyMixin(object):

    def __init__(self, proxies=None):
        self._proxies = proxies
        self._logger = logging.getLogger('proxies')
        self._fitness = None

    @property
    def proxies(self):
        if not self._proxies:
            self._proxies = tuple(map(lambda ip: 'http://' + ip, PROXY_IPs))
        return self._proxies

    @property
    def fitness(self):
        if not self._fitness:
            self._fitness = {proxy: DEFAULT_FITNESS for proxy in self.proxies}
        return self._fitness

    def _decrease_fitness(self, proxy):
        if proxy and self.fitness[proxy] > MIN_FITNESS:
            self.fitness[proxy] -= 1

    def _increase_fitness(self, proxy):
        if proxy and self.fitness[proxy] < MAX_FITNESS:
            self.fitness[proxy] += 1

    def _prefixes(self):
        prefix_ls = list()
        acc, n = 0, sum(self.fitness.values())
        for _, fitness in self.fitness.items():
            acc += fitness / n
            prefix_ls.append(acc)
        assert acc == 1, 'Wrong roulette logic!'
        return prefix_ls

    def _roulette(self):
        """
        Method uses roulette algorithm to pick random proxy
        :return proxy: String, ip address of proxy
        """
        return self.proxies[bisect_left(self._prefixes(), random())]

    def pick_proxy(self):
        p = self._roulette()
        print(f'Picking proxy: {p}')
        return p


if __name__ == '__main__':
    p = ProxyMixin()
