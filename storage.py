"""
LEM v1.3 — Observation Storage (Provenance + Metadata Aware)
------------------------------------------------------------
Handles persistent storage of LEM observations with explicit data provenance,
optional timestamp overrides, and canonical metadata annotations.

Responsibilities:
- Append timestamped observations to CSV
- Create file and header if missing
- Preserve raw values exactly as computed
- Require data_source labeling for every row
- Allow historical timestamp overrides (Phase B)
- Support chain and token metadata annotations (Phase C.1.1)

No calculations, no aggregation, no interpretation.
"""

import os
import csv
from datetime import datetime
from config import DATA_DIR, LEM_LOG_FILE


# =========================
# CSV Schema (Append-Only)
# =========================

CSV_HEADER = [
    "timestamp_utc",
    "pair_address",
    "chain",
    "native_price_usd",
    "native_reserve",
    "lp_native_usd",
    "token_price_usd",
    "market_cap_usd",
    "lem",
    "lp_delta_usd",
    "lp_delta_pct",
    "data_source",
    "token_symbol",
    "token_name",
]


# =========================
# Storage Initialization
# =========================

def ensure_storage():
    """
    Ensure data directory and CSV file exist.
    Creates them if missing.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(LEM_LOG_FILE):
        with open(LEM_LOG_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


# =========================
# Append Observation
# =========================

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
    chain: str | None = None,
    token_symbol: str | None = None,
    token_name: str | None = None,
    timestamp_override: str | None = None,
):
    """
    Append a single LEM observation row.

    Parameters:
    - data_source (required):
        Explicit provenance label, e.g.:
        - "reconstructed_gecko"
        - "onchain_live"

    - chain (optional):
        Canonical chain identifier, e.g. "bsc", "ethereum"

    - token_symbol / token_name (optional):
        Human-readable annotations (non-canonical metadata)

    - timestamp_override (optional):
        Used ONLY for historical backfills (Phase B)
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
            chain or "",
            native_price_usd,
            native_reserve,
            lp_native_usd,
            token_price_usd,
            market_cap_usd,
            lem,
            lp_delta_usd,
            lp_delta_pct,
            data_source,
            token_symbol or "",
            token_name or "",
        ])