from abc import ABC, abstractmethod
from ..assets import Portfolio


class Actor(ABC):
    """ Our base actor performs a strategy for some portfolio. """

    def __init__(self, portfolio, strategy):
        self.portfolio = portfolio
        self._strategy = strategy

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self, portfolio):
        if not isinstance(portfolio, Portfolio):
            raise TypeError("expected portfolio instance")
        self._portfolio = portfolio

    def perform(self):
        self._strategy.run()


class Strategy(ABC):
    @abstractmethod
    def run(self):
        pass
