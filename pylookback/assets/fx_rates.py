"""
Assets are setup such that they track their local value.
However, portfolios may consist of assets denominated in different currencies.
We'll need to value all assets in a chosen base currency.
To do this we need to keep track of FX rates.
"""
from weakref import WeakValueDictionary
from ..descriptors import StringOfFixedSize, UnsignedReal


class FxRate():
    """ Keep track of fx rates to value assets in different currencies. """
    _instances = WeakValueDictionary()

    # descriptors
    _currency_pair = StringOfFixedSize("_currency_pair", size=6)
    rate = UnsignedReal("rate")

    def __init__(self, currency_pair, rate):
        self._currency_pair = currency_pair
        self.rate = rate
        self._instances[currency_pair] = self

    @property
    def currency_pair(self):
        """ This is read only. """
        return self._currency_pair

    @classmethod
    def get(cls, currency_pair):
        if not isinstance(currency_pair, str):
            raise TypeError("expected str")
        if len(currency_pair) != 6:
            raise ValueError("expected a 6 character code")
        currency_pair = currency_pair.upper()

        ccy1 = currency_pair[:3]
        ccy2 = currency_pair[3:]
        if ccy1 == ccy2:
            return 1.0

        fx = cls._instances.get(currency_pair)
        if fx is None:
            raise ValueError("%s rate not available" % currency_pair)
        return fx.rate
