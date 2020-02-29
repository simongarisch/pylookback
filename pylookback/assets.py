from numbers import Real


class Asset:
    """ Portfolios consist of holdings (units of some asset).
        All assets should have a unique code (string) and a price (numeric).
    """
    def __init__(self, code, price):
        if not isinstance(code, str):
            raise TypeError("expected str")
        if not isinstance(price, Real):
            raise TypeError("expected numeric price")
        self.code = code
        self.price = price
