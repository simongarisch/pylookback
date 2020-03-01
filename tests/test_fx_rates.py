import pytest
from pylookback import FxRate


def test_fx_rate_init():
    fx = FxRate("AUDUSD", 0.65)
    assert fx.currency_pair == "AUDUSD"
    assert fx.rate == 0.65


def test_fx_rate_positive():
    fx = FxRate("AUDUSD", 0.65)
    assert fx.rate == 0.65
    fx.rate = 0.75
    assert fx.rate == 0.75
    with pytest.raises(ValueError):
        fx.rate = -0.85
    assert fx.rate == 0.75


def test_fx_currency_pair_read_only():
    fx = FxRate("AUDUSD", 0.65)
    with pytest.raises(AttributeError):
        fx.currency_pair = "AUDAUD"
