import abc


class BaseCrawler(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def crawl(self, *args, **kwargs):
        raise NotImplementedError()
