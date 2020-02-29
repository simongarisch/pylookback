import pytest
from pylookback import Asset


def test_init():
    asset = Asset("AAA US", 2.50)
    assert asset.code == "AAA US"
    assert asset.price == 2.50


def test_code_is_string():
    with pytest.raises(TypeError):
        Asset(110, 2.50)


def test_price_is_numeric():
    with pytest.raises(TypeError):
        Asset("AAA US", "2.50")
