import pytest
from pylookback import Cash


def test_init():
    usd = Cash("USD")
    assert usd.code == "USD"
    assert usd.currency_code == "USD"
    assert usd.price == 1
    assert usd.local_value == 1


def test_price_valid():
    gbp = Cash("GBP")
    assert gbp.code == "GBP"
    assert gbp.currency_code == "GBP"
    assert gbp.price == 1
    assert gbp.local_value == 1
    with pytest.raises(ValueError):
        gbp.price = 2.0
    assert gbp.price == 1


def test_currency_code_length():
    with pytest.raises(ValueError):
        Cash("GBPX")


def test_codes_uppercase():
    gbp = Cash("gbp")
    assert gbp.code == "GBP"
