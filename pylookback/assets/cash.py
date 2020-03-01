from .asset import Asset


class Cash(Asset):
    """ The local value for cash should always be 1.0. """
    def __init__(self, code):
        super().__init__(
            code=code,
            price=1.0,
            currency_code=code,
        )
        self._price = self._local_value = 1.0

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        """ Price and value (in local currency)
            for cash should be static.
        """
        if price != 1:
            raise ValueError("price should always be 1 for cash")

    def revalue(self):
        self._local_value = 1.0
