"""
LEM v1.0 — Observation Engine
----------------------------
Canonical observation loop for the Liquidity Elasticity Model.

Responsibilities:
- Load configuration
- Pull on-chain data
- Compute LPₙ, MC, LEM, ΔLPₙ
- Persist observations
- Sleep and repeat

This engine is READ-ONLY and NON-TRADING by design.
"""

import time

from config import OBSERVATION_INTERVAL
from price_oracle import get_native_asset_price_usd
from liquidity import get_native_reserve, calculate_lp_native_usd
from marketcap import calculate_token_price_usd, calculate_market_cap_usd
from lem import calculate_lem, calculate_lp_delta
from storage import append_observation


def run_engine(pair_address: str):
    """
    Run the LEM observation engine for a single AMM pair.

    Args:
        pair_address: AMM pair contract address
    """
    previous_lp_native_usd = None

    print("LEM Engine started.")
    print(f"Tracking pair: {pair_address}")
    print(f"Observation interval: {OBSERVATION_INTERVAL} seconds")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            # --- Step 1: Native asset USD price ---
            native_price_usd = get_native_asset_price_usd()

            # --- Step 2: Native reserve & LPₙ ---
            native_reserve = get_native_reserve(pair_address)
            lp_native_usd = calculate_lp_native_usd(
                pair_address, native_price_usd
            )

            # --- Step 3: Token price & Market Cap ---
            token_price_usd = calculate_token_price_usd(
                pair_address, native_price_usd
            )
            market_cap_usd = calculate_market_cap_usd(
                pair_address, native_price_usd
            )

            # --- Step 4: LEM & ΔLPₙ ---
            lem_value = calculate_lem(market_cap_usd, lp_native_usd)
            lp_delta = calculate_lp_delta(
                current_lp_native_usd=lp_native_usd,
                previous_lp_native_usd=previous_lp_native_usd,
            )

            # --- Step 5: Persist observation ---
            append_observation(
                pair_address=pair_address,
                native_price_usd=native_price_usd,
                native_reserve=native_reserve,
                lp_native_usd=lp_native_usd,
                token_price_usd=token_price_usd,
                market_cap_usd=market_cap_usd,
                lem=lem_value,
                lp_delta_usd=lp_delta["delta_usd"],
                lp_delta_pct=lp_delta["delta_pct"],
                data_source="onchain_live",
            )

            # --- Update state ---
            previous_lp_native_usd = lp_native_usd

            print(
                f"[OK] LEM={lem_value:.4f} | "
                f"LPₙ=${lp_native_usd:,.2f} | "
                f"MC=${market_cap_usd:,.2f}"
            )

        except Exception as e:
            # Engine must never crash silently
            print(f"[ERROR] {e}")

        # --- Sleep until next observation ---
        time.sleep(OBSERVATION_INTERVAL)


if __name__ == "__main__":
    # Replace with the AMM pair you want to observe
    TEST_PAIR = "0x58F876857a02D6762E0101bb5C46A8c1ED44Dc16"
    run_engine(TEST_PAIR)