import logging.config

from itertools import takewhile
from random import choice, random
from settings import LOGGING, PROXY_IPS, DEFAULT_FITNESS, MINIMAL_FITNESS, MAXIMAL_FITNESS

logging.config.dictConfig(LOGGING)


class ProxyMixin(object):

    def __init__(self, proxies=None):
        self._proxies = proxies
        self._logger = logging.getLogger('proxies')
        self._fitness = None

    @property
    def proxies(self):
        if not self._proxies:
            self._proxies = tuple(map(lambda ip: 'http://' + ip, PROXY_IPS))
        return self._proxies

    @property
    def fitness(self):
        if not self._fitness:
            self._fitness = {proxy: DEFAULT_FITNESS for proxy in self.proxies}
        return self._fitness

    @staticmethod
    def _reduce_gen(ls):
        current_sum = 0
        for x in ls:
            current_sum += x
            yield current_sum

    def _diminish_fitness(self, proxy):
        if self.fitness[proxy] > MINIMAL_FITNESS:
            self.fitness[proxy] -= .01

    def _increase_fitness(self, proxy):
        if self.fitness[proxy] < MAXIMAL_FITNESS:
            self.fitness[proxy] += .01

    def _roulette(self):
        r = random()
        curr_sum = 0
        for proxy, fitness in self.fitness.items():
            curr_sum += fitness
            if curr_sum >= r:
                return proxy
        return choice(self.proxies)

    def pick_proxy(self):
        pass
        # return self.roulette_pick()


if __name__ == '__main__':
    p = ProxyMixin()
