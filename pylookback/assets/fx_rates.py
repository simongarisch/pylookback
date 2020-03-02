"""
Assets are setup such that they track their local value.
However, portfolios may consist of assets denominated in different currencies.
We'll need to value all assets in a chosen base currency.
To do this we need to keep track of FX rates.
"""
from weakref import WeakValueDictionary
from ..observable import Observable
from ..descriptors import StringOfFixedSize, UnsignedReal


def validate_pair(currency_pair):
    if not isinstance(currency_pair, str):
        raise TypeError("expected str")
    currency_pair = currency_pair.strip()
    if len(currency_pair) != 6:
        raise ValueError("expected a 6 character code")


def is_equivalent_pair(currency_pair):
    """ Returns True where we expect the rate to be static.
        For example, AUDAUD = 1.0, USDUSD = 1.0
    >>> is_equivalent_pair("AUDAUD")
    True
    >>> is_equivalent_pair("AUDUSD")
    False
    """
    validate_pair(currency_pair)
    ccy1 = currency_pair[:3]
    ccy2 = currency_pair[3:]
    if ccy1 == ccy2:
        return True
    return False


class FxRate(Observable):
    """ Keep track of fx rates to value assets in different currencies. """

    _instances = WeakValueDictionary()

    # descriptors
    _currency_pair = StringOfFixedSize("_currency_pair", size=6)
    _rate = UnsignedReal("_rate")

    def __init__(self, currency_pair, rate):
        super().__init__()
        if not isinstance(currency_pair, str):
            raise TypeError("expected str")
        currency_pair = currency_pair.strip().upper()

        self._currency_pair = currency_pair
        self.rate = rate
        if currency_pair in self._instances:
            raise ValueError("%s already created" % currency_pair)
        self._instances[currency_pair] = self

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate
        self.notify_observers()

    @property
    def currency_pair(self):
        """ This is read only. """
        return self._currency_pair

    @classmethod
    def get(cls, currency_pair):
        validate_pair(currency_pair)
        currency_pair = currency_pair.strip().upper()

        if is_equivalent_pair(currency_pair):
            return 1.0

        fx = cls._instances.get(currency_pair)
        if fx is None:
            raise ValueError("%s rate not available" % currency_pair)
        return fx.rate
