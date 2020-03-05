from numbers import Real
from .asset import Asset
from .cash import Cash
from .fx_rates import FxRate, is_equivalent_pair
from ..observable import Observable
from ..descriptors import Integer, StringOfFixedSize


class Holding(Observable):
    """ Hold units in some asset.
        The base currency code defines the currency in which this holding
        will be valued.
    """

    _units = Integer("_units")
    _base_currency_code = StringOfFixedSize("_base_currency_code", size=3)

    def __init__(self, asset, units, base_currency_code):
        super().__init__()
        if not isinstance(asset, Asset):
            raise TypeError("expected asset")
        self._asset = asset
        self._asset_code = asset.code
        self._asset_currency_code = asset.currency_code
        self._base_currency_code = base_currency_code
        self._observe_components()
        self._currency_pair = asset.currency_code + base_currency_code
        self._local_currency_value = self._base_currency_value = None
        self.units = units

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = units
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
        self.notify_observers()

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

    def __str__(self):
        return (
            "Holding -> "
            + self._asset_code
            + ", "
            + str(self.units)
            + ", "
            + self._base_currency_code
            + ", "
            + str(self._base_currency_value)
        )


class Portfolio(Asset):
    _base_currency_code = StringOfFixedSize("_base_currency_code", size=3)

    def __init__(self, base_currency_code="USD"):
        self._holdings = dict()
        self._base_currency_code = base_currency_code
        self._value = 0

    @property
    def base_currency_code(self):
        return self._base_currency_code

    @property
    def value(self):
        return self._value

    def transfer(self, asset, units):
        self._change_holdings(asset, units)

    def trade(self, asset, units, consideration=None):
        if consideration is None:
            consideration = asset.local_currency_value * -units
        else:
            if not isinstance(consideration, Real):
                raise TypeError("expecting numeric consideration")

        currency_code = asset.currency_code
        if Asset.asset_code_exists(currency_code):
            cash = Asset.get_asset_by_code(currency_code)
        else:
            cash = Cash(currency_code)
        self._change_holdings(cash, consideration)
        self._change_holdings(asset, units)

    def _change_holdings(self, asset, units):
        asset_code = asset.code
        if asset_code in self._holdings:
            holding = self._holdings[asset_code]
            holding.units += units
        else:
            holding = Holding(asset, units, self._base_currency_code)
            holding.add_observer(self)
            self._holdings[asset_code] = holding
        self._revalue()

    def observable_update(self, observable):
        self._revalue()

    def _revalue(self):
        value = 0
        for _, holding in self._holdings.items():
            value += holding.base_currency_value
        self._value = value

    def __str__(self):
        return "Portfolio -> " + "\n".join(
            [
                code + ": " + str(holding.units)
                for code, holding in self._holdings.items()
            ]
        )
