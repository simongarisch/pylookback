import pytest
from pylookback import Asset, Stock


def test_init():
    asset = Stock("AAA US", 2.50, "USD")
    assert asset.code == "AAA US"
    assert asset.price == 2.50
    assert asset.local_value == 2.50


def test_code_is_string():
    with pytest.raises(TypeError):
        Stock(110, 2.50)


def test_price_is_numeric():
    with pytest.raises(TypeError):
        Stock("BBB US", "2.50", "USD")
    with pytest.raises(ValueError):
        Stock("BBB US", -2.50, "USD")


def test_currency_code():
    with pytest.raises(TypeError):
        Stock("CCC US", 2.50, 100)
    with pytest.raises(ValueError):
        Stock("DDD US", 2.50, "USDA")


def test_code_recycle():
    stock = Stock("ZZZ AU", 2.50, "AUD")
    assert stock.code == "ZZZ AU"
    with pytest.raises(ValueError):
        # we cannot create a stock with the same code
        Stock("ZZZ AU", 2.50, "AUD")

    # after deletion the code is recycled
    del stock

    # now recreating the stock should not raise errors
    Stock("ZZZ AU", 2.50, "AUD")


def test_registered_codes():
    num_codes = len(Asset.registered_codes())
    zzb = Stock("ZZB AU", 2.50, "AUD")
    assert len(Asset.registered_codes()) == num_codes + 1
    del zzb
    assert len(Asset.registered_codes()) == num_codes
