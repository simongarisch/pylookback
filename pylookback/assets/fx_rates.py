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


def split_pair(currency_pair):
    """ Return two individual components of the pair.
    >>> split_pair("AUDUSD")
    ('AUD', 'USD')
    """
    validate_pair(currency_pair)
    ccy1 = currency_pair[:3]
    ccy2 = currency_pair[3:]
    return ccy1, ccy2


def is_equivalent_pair(currency_pair):
    """ Returns True where we expect the rate to be static.
        For example, AUDAUD = 1.0, USDUSD = 1.0
    >>> is_equivalent_pair("AUDAUD")
    True
    >>> is_equivalent_pair("AUDUSD")
    False
    """
    ccy1, ccy2 = split_pair(currency_pair)
    if ccy1 == ccy2:
        return True
    return False


def get_inverse_pair(currency_pair):
    """ Returns the inverse of some currency pair.
    >>> get_inverse_pair("AUDUSD")
    'USDAUD'
    """
    ccy1, ccy2 = split_pair(currency_pair)
    return ccy2 + ccy1


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

        inverse_pair = get_inverse_pair(currency_pair)
        if inverse_pair in self._instances:
            raise ValueError("%s inverse pair already created" % inverse_pair)
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
        if fx is not None:
            return fx.rate

        inverse_pair = get_inverse_pair(currency_pair)
        fx = cls._instances.get(inverse_pair)
        if fx is not None:
            return 1 / fx.rate

        raise ValueError("%s rate not available" % currency_pair)

    @classmethod
    def get_instance(cls, currency_pair):
        validate_pair(currency_pair)
        instance = cls._instances.get(currency_pair)
        if instance is None:
            raise ValueError("%s instance doesn't exist" % currency_pair)
        return instance

    @classmethod
    def get_observable_instance(cls, currency_pair):
        """ Return an instance representing either the
            currency pair (if available) or its inverse.
        """
        validate_pair(currency_pair)
        instance = cls._instances.get(currency_pair)
        if instance is not None:
            return instance

        inverse_pair = get_inverse_pair(currency_pair)
        instance = cls._instances.get(inverse_pair)
        if instance is not None:
            return instance

        raise ValueError("%s instance doesn't exist" % currency_pair)
