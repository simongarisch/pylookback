from numbers import Real


class Asset:
    """ Portfolios consist of holdings (units of some asset).
        All assets should have a unique code (string) and a price (numeric).
    """
    def __init__(self, code, price, currency_code="USD"):
        if not isinstance(code, str):
            raise TypeError("expected string for asset code")
        if not isinstance(price, Real):
            raise TypeError("expected numeric price")
        if not isinstance(currency_code, str):
            raise TypeError("expected string for currency code")
        if len(currency_code) != 3:
            raise ValueError("currency codes should be 3 characters long")
        self.code = code
        self.price = price
        self.currency_code = currency_code
