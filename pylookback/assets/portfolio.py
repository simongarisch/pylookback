from .asset import Asset
from .fx_rates import FxRate, is_equivalent_pair
from ..observable import Observable
from ..descriptors import Integer, StringOfFixedSize


class Holding(Observable):
    """ Hold units in some asset.
        The base currency code defines the currency in which this holding
        will be valued.
    """

    units = Integer("units")
    _base_currency_code = StringOfFixedSize("_base_currency_code", size=3)

    def __init__(self, asset, units, base_currency_code):
        super().__init__()
        if not isinstance(asset, Asset):
            raise TypeError("expected asset")
        self._asset = asset
        self.units = units
        self._asset_code = asset.code
        self._asset_currency_code = asset.currency_code
        self._base_currency_code = base_currency_code
        self._observe_components()
        self._currency_pair = asset.currency_code + base_currency_code
        self._local_currency_value = self._base_currency_value = None
        self._revalue()

    def _observe_components(self):
        self._asset.add_observer(self)
        currency_pair = self.asset_currency_code + self.base_currency_code
        if not is_equivalent_pair(currency_pair):
            fx_instance = FxRate.get_observable_instance(currency_pair)
            fx_instance.add_observer(self)

    def observable_update(self, observable):
        self._revalue()

    def _revalue(self):
        self._local_currency_value = self._asset.local_value * self.units
        fx_rate = FxRate.get(self._currency_pair)
        self._base_currency_value = self._local_currency_value * fx_rate

    @property
    def asset_code(self):
        return self._asset_code

    @property
    def asset_currency_code(self):
        return self._asset_currency_code

    @property
    def base_currency_code(self):
        return self._base_currency_code

    @property
    def local_currency_value(self):
        return self._local_currency_value

    @property
    def base_currency_value(self):
        return self._base_currency_value


class Portfolio(Asset):
    pass
