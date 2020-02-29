from weakref import WeakSet
from abc import ABC, abstractmethod
from ..descriptors import String, UnsignedReal, StringOfFixedSize


class Asset(ABC):
    """ Portfolios consist of holdings (units of some asset).
        All assets should have:
        - a unique code (string)
        - a price (numeric)
        - a quoted currency code (e.g. 'USD', 'EUR', 'AUD')
        - a local value (or value in quoted currency)

        Code and currency_code are static and should not change
        over the asset's life.
    """
    _instances = WeakSet()

    # descriptors
    _code = String("_code")
    _currency_code = StringOfFixedSize("_currency_code", size=3)
    price = UnsignedReal("price")

    @classmethod
    def _register_asset(cls, asset):
        cls._instances.add(asset)

    @classmethod
    def registered_codes(cls):
        return sorted([asset.code for asset in cls._instances])

    def _validate_code(self, code):
        """ Every asset must have a unique string code. """
        if code in self.registered_codes():
            raise ValueError("Code %s is already in use" % code)
        self._code = code
        self._register_asset(self)

    def __init__(self, code, price, currency_code):
        self._validate_code(code)
        self._currency_code = currency_code
        self._local_value = None
        self.price = price

    @property
    def code(self):
        return self._code

    @property
    def currency_code(self):
        return self._currency_code

    @property
    def local_value(self):
        return self._local_value

    @abstractmethod
    def revalue(self):
        """ Each concrete asset must define its own revalue method. """
        raise NotImplementedError()
