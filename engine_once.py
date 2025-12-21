"""
LEM Phase C — Single Observation Engine
--------------------------------------
Runs ONE on-chain observation and exits.
Designed for GitHub Actions cron execution.

Phase C.1.1:
- Adds explicit chain context
- Adds token symbol and token name annotations
"""

from config import CHAIN
from chain import get_base_token_address, get_token_metadata
from price_oracle import get_native_asset_price_usd
from liquidity import calculate_lp_native_usd
from marketcap import calculate_token_price_usd, calculate_market_cap_usd
from lem import calculate_lem
from storage import append_observation


# =========================
# CONFIG
# =========================

PAIR_ADDRESS = "0x933477eba23726ca95a957cb85dbb1957267ef85"
DATA_SOURCE = "onchain_live"


def run_once():
    # 1. Fetch native asset price (USD)
    native_price = get_native_asset_price_usd()

    # 2. Calculate native liquidity (LPₙ)
    #    liquidity.py resolves reserves and native side internally
    lp_native_usd = calculate_lp_native_usd(PAIR_ADDRESS, native_price)

    # 3. Calculate token price (USD)
    token_price = calculate_token_price_usd(PAIR_ADDRESS, native_price)

    # 4. Calculate market cap (USD)
    market_cap = calculate_market_cap_usd(PAIR_ADDRESS, native_price)

    # 5. Calculate LEM
    lem_value = calculate_lem(market_cap, lp_native_usd)

    # 6. Resolve base token and metadata (annotations)
    base_token = get_base_token_address(PAIR_ADDRESS)
    meta = get_token_metadata(base_token)

    token_symbol = meta["symbol"]
    token_name = meta["name"]

    # 7. Append observation (single atomic row)
    append_observation(
        pair_address=PAIR_ADDRESS,
        native_price_usd=native_price,
        native_reserve=None,
        lp_native_usd=lp_native_usd,
        token_price_usd=token_price,
        market_cap_usd=market_cap,
        lem=lem_value,
        lp_delta_usd=None,
        lp_delta_pct=None,
        data_source=DATA_SOURCE,
        chain=CHAIN,
        token_symbol=token_symbol,
        token_name=token_name,
    )


if __name__ == "__main__":
    run_once()