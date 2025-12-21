"""
LEM v1.2 — Observation Storage (Provenance + Timestamp Aware)
-------------------------------------------------------------
Handles persistent storage of LEM observations with explicit data provenance
and optional timestamp overrides.

Responsibilities:
- Append timestamped observations to CSV
- Create file and header if missing
- Preserve raw values exactly as computed
- Require data_source labeling for every row
- Allow historical timestamp overrides (Phase B)

No calculations, no aggregation, no interpretation.
"""

import os
import csv
from datetime import datetime
from config import DATA_DIR, LEM_LOG_FILE


CSV_HEADER = [
    "timestamp_utc",
    "pair_address",
    "native_price_usd",
    "native_reserve",
    "lp_native_usd",
    "token_price_usd",
    "market_cap_usd",
    "lem",
    "lp_delta_usd",
    "lp_delta_pct",
    "data_source",
]


def ensure_storage():
    """Ensure data directory and CSV file exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(LEM_LOG_FILE):
        with open(LEM_LOG_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def append_observation(
    pair_address: str,
    native_price_usd: float,
    native_reserve: float,
    lp_native_usd: float,
    token_price_usd: float,
    market_cap_usd: float,
    lem: float,
    lp_delta_usd,
    lp_delta_pct,
    data_source: str,
    timestamp_override: str | None = None,
):
    """
    Append a single LEM observation row.

    data_source must explicitly identify provenance, e.g.:
    - "reconstructed_gecko"
    - "onchain_live"

    timestamp_override is optional and used ONLY for historical backfills.
    """
    if not data_source:
        raise ValueError("data_source must be provided")

    ensure_storage()

    timestamp = timestamp_override or datetime.utcnow().isoformat()

    with open(LEM_LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            pair_address,
            native_price_usd,
            native_reserve,
            lp_native_usd,
            token_price_usd,
            market_cap_usd,
            lem,
            lp_delta_usd,
            lp_delta_pct,
            data_source,
        ])