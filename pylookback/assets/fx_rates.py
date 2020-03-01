"""
Assets are setup such that they track their local value.
However, portfolios may consist of assets denominated in different currencies.
We'll need to value all assets in a chosen base currency.
To do this we need to keep track of FX rates.
"""
from ..descriptors import StringOfFixedSize, UnsignedReal


class FxRate():
    _currency_pair = StringOfFixedSize("_currency_pair", size=6)
    rate = UnsignedReal("rate")

    def __init__(self, currency_pair, rate):
        self._currency_pair = currency_pair
        self.rate = rate

    @property
    def currency_pair(self):
        """ This is read only. """
        return self._currency_pair


class FxRates():
    pass
