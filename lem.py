"""
LEM v1.0 — Liquidity Elasticity Model Core
-----------------------------------------
Implements the canonical Liquidity Elasticity Model.

Responsibilities:
- Compute Liquidity Elasticity Coefficient (LEM)
- Compute Native Liquidity Delta (ΔLPₙ)
- Provide normalized outputs for downstream use

This module contains NO I/O, NO storage, and NO trading logic.
"""

from typing import Optional


def calculate_lem(market_cap_usd: float, lp_native_usd: float) -> float:
    """
    Calculate the Liquidity Elasticity Coefficient (LEM).

    LEM = Market Capitalization (USD) / Native Liquidity (USD)

    Args:
        market_cap_usd: Market capitalization in USD
        lp_native_usd: Native liquidity (LPₙ) in USD

    Returns:
        float: Liquidity Elasticity Coefficient

    Raises:
        ValueError if inputs are invalid
    """
    if market_cap_usd <= 0:
        raise ValueError("market_cap_usd must be > 0")

    if lp_native_usd <= 0:
        raise ValueError("lp_native_usd must be > 0")

    return float(market_cap_usd / lp_native_usd)


def calculate_lp_delta(
    current_lp_native_usd: float,
    previous_lp_native_usd: Optional[float],
) -> dict:
    """
    Calculate Native Liquidity Delta (ΔLPₙ).

    ΔLPₙ = LPₙ(t) − LPₙ(t−1)
    ΔLPₙ% = (LPₙ(t) − LPₙ(t−1)) / LPₙ(t−1)

    Args:
        current_lp_native_usd: Current LPₙ value in USD
        previous_lp_native_usd: Previous LPₙ value in USD (or None if unavailable)

    Returns:
        dict:
            {
                "delta_usd": float | None,
                "delta_pct": float | None
            }
    """
    if current_lp_native_usd <= 0:
        raise ValueError("current_lp_native_usd must be > 0")

    # First observation has no delta
    if previous_lp_native_usd is None:
        return {
            "delta_usd": None,
            "delta_pct": None,
        }

    if previous_lp_native_usd <= 0:
        raise ValueError("previous_lp_native_usd must be > 0")

    delta_usd = current_lp_native_usd - previous_lp_native_usd
    delta_pct = delta_usd / previous_lp_native_usd

    return {
        "delta_usd": float(delta_usd),
        "delta_pct": float(delta_pct),
    }