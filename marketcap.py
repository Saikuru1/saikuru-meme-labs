"""
LEM v1.0 — Market Capitalization
-------------------------------
Implements Steps 5 and 6 of the LEM paper.

Responsibilities:
- Compute implied token price from AMM reserves
- Compute Market Capitalization (MC)

No liquidity ratios, no LEM, no deltas.
"""

from chain import (
    get_pair_tokens,
    get_pair_reserves,
    get_total_supply,
    get_token_decimals,
    normalize_reserve,
)
from liquidity import identify_native_side


def calculate_token_price_usd(pair_address: str, native_price_usd: float) -> float:
    """
    Calculate the implied token price in USD using AMM reserves.

    Price_token = (Reserve_native / Reserve_token) * Price_native(USD)

    Args:
        pair_address: AMM pair address
        native_price_usd: USD price of the native chain asset

    Returns:
        float: Token price in USD
    """
    if native_price_usd <= 0:
        raise ValueError("native_price_usd must be > 0")

    side = identify_native_side(pair_address)
    reserves = get_pair_reserves(pair_address)

    token0 = side["token0"]
    token1 = side["token1"]

    # Determine raw reserves
    if side["native_is_token0"]:
        raw_native = reserves["reserve0"]
        raw_token = reserves["reserve1"]
        token_address = token1
    else:
        raw_native = reserves["reserve1"]
        raw_token = reserves["reserve0"]
        token_address = token0

    native_decimals = get_token_decimals(
        token0 if side["native_is_token0"] else token1
    )
    token_decimals = get_token_decimals(token_address)

    native_reserve = normalize_reserve(raw_native, native_decimals)
    token_reserve = normalize_reserve(raw_token, token_decimals)

    if token_reserve <= 0:
        raise ValueError("Token reserve must be > 0")

    token_price_usd = (native_reserve / token_reserve) * float(native_price_usd)

    return float(token_price_usd)


def calculate_market_cap_usd(pair_address: str, native_price_usd: float) -> float:
    """
    Calculate Market Capitalization (MC) in USD.

    MC = Total Circulating Supply × Token Price (USD)

    Args:
        pair_address: AMM pair address
        native_price_usd: USD price of the native chain asset

    Returns:
        float: Market Capitalization in USD
    """
    token_price_usd = calculate_token_price_usd(pair_address, native_price_usd)

    side = identify_native_side(pair_address)
    token_address = side["token1"] if side["native_is_token0"] else side["token0"]

    total_supply = get_total_supply(token_address)

    market_cap = total_supply * token_price_usd

    return float(market_cap)