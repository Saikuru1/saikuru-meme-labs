"""
LEM v1.0 — Native Asset Price Oracle
-----------------------------------
This module retrieves the USD price of the native chain asset.

Responsibilities:
- Fetch native asset USD price
- Return clean float
- Handle API failure safely

This module must NEVER fetch token prices.
"""

import requests
from config import COINGECKO_NATIVE_PRICE_URL


def get_native_asset_price_usd() -> float:
    """
    Fetch the USD price of the native blockchain asset.

    Returns:
        float: Native asset price in USD

    Raises:
        RuntimeError if price cannot be retrieved
    """
    try:
        response = requests.get(COINGECKO_NATIVE_PRICE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch native asset price: {e}")

    try:
        # For BNB Chain, CoinGecko uses 'binancecoin'
        price_usd = data["binancecoin"]["usd"]
    except (KeyError, TypeError):
        raise RuntimeError("Malformed response from price oracle")

    if price_usd <= 0:
        raise RuntimeError("Invalid native asset price received")

    return float(price_usd)