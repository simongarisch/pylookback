import pytest
from pylookback.assets import Portfolio, Stock, Cash, FxRate


def test_portfolio_init():
    portfolio = Portfolio("AUD")
    assert portfolio.base_currency_code == "AUD"
    assert portfolio.value == 0


def test_base_currency():
    with pytest.raises(TypeError):
        Portfolio(123)
    with pytest.raises(ValueError):
        Portfolio("AUDX")
    portfolio = Portfolio("AUD")
    assert portfolio.base_currency_code == "AUD"


def test_transfer_cash():
    portfolio = Portfolio("AUD")
    assert portfolio.value == 0

    aud = Cash("AUD")
    usd = Cash("USD")
    audusd = FxRate("AUDUSD", 0.65)

    portfolio.transfer(aud, 1000)
    assert portfolio.value == 1000

    portfolio.transfer(usd, 1000)
    assert portfolio.value == 1000 + 1000 / audusd.rate


def test_transfer_stock():
    portfolio = Portfolio("AUD")
    assert portfolio.value == 0
    zzb = Stock("ZZB AU", 2.50, "AUD")
    portfolio.transfer(zzb, 1000)
    assert portfolio.value == 1000 * 2.50

    aapl = Stock("AAPL US", 300, "USD")
    audusd = FxRate("AUDUSD", 0.65)
    portfolio.transfer(aapl, 1000)
    assert portfolio.value, 2 == 1000 * 2.50 + 1000 * 300 / audusd.rate

    portfolio.transfer(aapl, -1000)
    assert portfolio.value == 1000 * 2.50  # just zzb left

    portfolio.transfer(zzb, -1000)
    assert portfolio.value == 0


def test_cash_holdings_observed():
    portfolio = Portfolio("AUD")
    assert portfolio.value == 0

    aud = Cash("AUD")
    portfolio.transfer(aud, 1000)
    assert portfolio.value == 1000

    usd = Cash("USD")
    audusd = FxRate("AUDUSD", 0.65)
    portfolio.transfer(usd, 1000)
    assert portfolio.value == 1000 + 1000 / audusd.rate
    audusd.rate == 0.55
    assert portfolio.value == 1000 + 1000 / audusd.rate
    audusd.rate == 0.75
    assert portfolio.value == 1000 + 1000 / audusd.rate
