from weakref import WeakSet
from abc import ABC, abstractmethod
from ..observable import Observable
from ..descriptors import String, UnsignedReal, StringOfFixedSize


class Asset(ABC, Observable):
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
    _price = UnsignedReal("_price")

    @classmethod
    def _register_asset(cls, asset):
        cls._instances.add(asset)

    @classmethod
    def registered_codes(cls):
        return sorted([asset.code for asset in cls._instances])

    @classmethod
    def asset_code_exists(cls, code):
        return code in cls.registered_codes()

    @classmethod
    def get_asset_by_code(cls, code):
        for asset in cls._instances:
            if asset.code == code:
                return asset
        raise ValueError("code %s does not exist" % code)

    def _validate_code(self, code):
        """ Every asset must have a unique string code. """
        if code in self.registered_codes():
            raise ValueError("Code %s is already in use" % code)
        self._code = code
        self._register_asset(self)

    def __init__(self, code, price, currency_code):
        super().__init__()
        self._validate_code(code)
        self._currency_code = currency_code
        self._local_value = None
        self.price = price

    # code, currency_code and local value can be read but not set
    @property
    def code(self):
        return self._code

    @property
    def currency_code(self):
        return self._currency_code

    @property
    def local_value(self):
        return self._local_value

    # changes in price will trigger the abstract method 'revalue'
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        """ Call the revalue method when price changes. """
        self._price = price
        self.revalue()

    def revalue(self):
        """ After calling the internal revalue method take
            the extra step of notifying observers.
        """
        self._revalue()
        self.notify_observers()

    @abstractmethod
    def _revalue(self):
        """ Each concrete asset must define its own revalue method. """
        raise NotImplementedError()
