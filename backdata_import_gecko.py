"""
LEM Phase B — GeckoTerminal Backdata Importer (Daily, Reconstructed)
-------------------------------------------------------------------
One-time script to seed historical LEM proxy data for Wiki Cat (WKC).

All rows written by this script are labeled:
    data_source = "reconstructed_gecko"

This script must NEVER be automated.
"""

import requests
from datetime import datetime
from storage import append_observation


# =========================
# CONFIGURATION
# =========================

NETWORK = "bsc"
POOL_ADDRESS = "0x933477eba23726ca95a957cb85dbb1957267ef85"
TIMEFRAME = "day"     # DAILY structural view
LIMIT = 1000          # ~3 years of daily data


# =========================
# API ENDPOINTS
# =========================

POOL_URL = (
    f"https://api.geckoterminal.com/api/v2/networks/{NETWORK}"
    f"/pools/{POOL_ADDRESS}"
)

OHLCV_URL = (
    f"https://api.geckoterminal.com/api/v2/networks/{NETWORK}"
    f"/pools/{POOL_ADDRESS}/ohlcv/{TIMEFRAME}"
    f"?limit={LIMIT}"
)


def fetch_json(url: str):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()


def run_import():
    print("Fetching pool snapshot...")
    pool = fetch_json(POOL_URL)["data"]["attributes"]

    market_cap = float(pool["market_cap_usd"])
    total_liquidity = float(pool["reserve_in_usd"])

    lp_native_proxy = total_liquidity / 2
    lem_proxy = market_cap / lp_native_proxy if lp_native_proxy > 0 else None

    print("Fetching daily OHLCV backdata...")
    candles = fetch_json(OHLCV_URL)["data"]["attributes"]["ohlcv_list"]
    print(f"Fetched {len(candles)} daily candles")

    for candle in candles:
        ts, _, _, _, close_price, _ = candle
        candle_timestamp = datetime.utcfromtimestamp(ts).isoformat()

        append_observation(
            pair_address=POOL_ADDRESS,
            native_price_usd=None,
            native_reserve=None,
            lp_native_usd=lp_native_proxy,
            token_price_usd=float(close_price),
            market_cap_usd=market_cap,
            lem=lem_proxy,
            lp_delta_usd=None,
            lp_delta_pct=None,
            data_source="reconstructed_gecko",
            timestamp_override=candle_timestamp,
        )

    print("Wiki Cat backdata import complete.")


if __name__ == "__main__":
    run_import()