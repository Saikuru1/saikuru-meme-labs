"""
LEM Phase D — Multi-Asset Observation Engine
--------------------------------------------
Runs ONE observation cycle across multiple AMM pairs and exits.
Designed for GitHub Actions cron execution.

Phase D additions:
- Tracks multiple pairs per run
- Isolates failures per asset (fault-tolerant)
- Appends one atomic row per asset
- Uses single canonical CSV, partitioned by pair_address

No trading logic. No alerts. Observation only.
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

DATA_SOURCE = "onchain_live"

# BNB Chain — Meme / Experimental Sample Set
PAIRS = [
    # Wiki Cat (mature reference asset)
    "0x933477eba23726ca95a957cb85dbb1957267ef85",

    # Shisa (very early-stage meme)
    "0x80d4150938dfac5313bb25eb4c121a40504617d0",

    # Hachiko
    "0xe6edc555061d1d9fe0145867b7ea7b07da840898",

    # Token called "4"
    "0xf0a949d3d93b833c183a27ee067165b6f2c9625e",

    # cBNB
    "0x37e8d5a7c7c95d1adc905e680ebd0c321b64ab13",
]


def run_once():
    # 1. Fetch native asset price (USD) once per run
    native_price = get_native_asset_price_usd()

    for pair_address in PAIRS:
        try:
            # 2. Native Liquidity (LPₙ)
            lp_native_usd = calculate_lp_native_usd(pair_address, native_price)

            # 3. Token price (USD)
            token_price = calculate_token_price_usd(pair_address, native_price)

            # 4. Market cap (USD)
            market_cap = calculate_market_cap_usd(pair_address, native_price)

            # 5. LEM
            lem_value = calculate_lem(market_cap, lp_native_usd)

            # 6. Resolve base token metadata (annotations only)
            base_token = get_base_token_address(pair_address)
            meta = get_token_metadata(base_token)

            token_symbol = meta.get("symbol", "")
            token_name = meta.get("name", "")

            # 7. Append observation (atomic per asset)
            append_observation(
                pair_address=pair_address,
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

        except Exception as e:
            # Fault isolation: one bad pair never kills the run
            print(f"[WARN] Skipping pair {pair_address}: {e}")


if __name__ == "__main__":
    run_once()