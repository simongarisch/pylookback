from pylookback.assets import Stock, Holding, FxRate


def test_holding_init():
    asset = Stock("AAA US", 2.50, "USD")
    audusd = FxRate("AUDUSD", 0.65)
    holding = Holding(asset, 100, "AUD")

    local_currency_value = 100 * 2.50
    base_currency_value = local_currency_value / audusd.rate
    assert holding.local_currency_value == local_currency_value
    assert holding.base_currency_value == base_currency_value
