"""
LEM v1.0 — Native Liquidity (LPₙ)
--------------------------------
Implements Section 2.1 of the LEM paper.

Responsibilities:
- Identify which reserve is the native asset
- Normalize reserves using token decimals
- Compute Native Liquidity (LPₙ) in USD

No market cap, no ratios, no trading logic.
"""

from web3 import Web3
from config import NATIVE_ASSET_ADDRESS
from chain import get_pair_tokens, get_pair_reserves, get_token_decimals, normalize_reserve


def identify_native_side(pair_address: str) -> dict:
    """
    Identify whether token0 or token1 is the native wrapped asset.

    Returns:
        {
            "native_is_token0": bool,
            "token0": str,
            "token1": str
        }

    Raises:
        ValueError if native asset is not part of the pair.
    """
    tokens = get_pair_tokens(pair_address)
    token0 = tokens["token0"]
    token1 = tokens["token1"]

    native = Web3.to_checksum_address(NATIVE_ASSET_ADDRESS)

    if token0 == native:
        return {"native_is_token0": True, "token0": token0, "token1": token1}
    if token1 == native:
        return {"native_is_token0": False, "token0": token0, "token1": token1}

    raise ValueError("Native asset not found in this pair (not a token/native pool).")


def get_native_reserve(pair_address: str) -> float:
    """
    Read the pair reserves and return the normalized native reserve quantity.

    Returns:
        float: Native reserve amount (e.g., WBNB quantity, not USD)

    Raises:
        ValueError if native asset is not part of the pair.
    """
    side = identify_native_side(pair_address)
    reserves = get_pair_reserves(pair_address)

    # Determine which token is native and which raw reserve corresponds to it
    if side["native_is_token0"]:
        native_token_address = side["token0"]
        raw_native_reserve = reserves["reserve0"]
    else:
        native_token_address = side["token1"]
        raw_native_reserve = reserves["reserve1"]

    native_decimals = get_token_decimals(native_token_address)
    native_reserve = normalize_reserve(raw_native_reserve, native_decimals)

    return float(native_reserve)


def calculate_lp_native_usd(pair_address: str, native_price_usd: float) -> float:
    """
    Calculate Native Liquidity (LPₙ) in USD.

    LPₙ = Reserveₙ × Priceₙ(USD)

    Args:
        pair_address: AMM pair address
        native_price_usd: USD price of the native chain asset (e.g., BNB/USD)

    Returns:
        float: Native Liquidity (LPₙ) in USD
    """
    if native_price_usd <= 0:
        raise ValueError("native_price_usd must be > 0")

    native_reserve = get_native_reserve(pair_address)
    lp_native_usd = native_reserve * float(native_price_usd)

    return float(lp_native_usd)