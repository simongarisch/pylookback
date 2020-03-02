from .asset import Asset
from ..observable import Observable
from ..descriptors import Integer


class Holding(Observable):
    """ Hold units in some asset. """

    units = Integer("units")

    def __init__(self, asset, units):
        super().__init__()
        if not isinstance(asset, Asset):
            raise TypeError("expected asset")
        self._asset = asset
        self._asset_code = asset.code
        self._asset_currency_code = asset.currency_code
        self.units = units

    @property
    def asset_code(self):
        return self._asset_code

    @property
    def asset_currency_code(self):
        return self._asset_currency_code


class Portfolio(Asset):
    pass
