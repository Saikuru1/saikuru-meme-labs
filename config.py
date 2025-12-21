"""
LEM v1.0 — Canonical Configuration
---------------------------------
This file defines all system-wide constants.
No logic is permitted in this file.
"""

# =========================
# Blockchain Configuration
# =========================

# Canonical chain identifier (used for research partitioning)
CHAIN = "bsc"

# BNB Chain public RPC (replace with private node later if desired)
RPC_URL = "https://bsc-dataseed.binance.org/"

# Native wrapped asset (WBNB)
NATIVE_ASSET_ADDRESS = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

# PancakeSwap V2 Factory (optional, not required for reserve reads)
FACTORY_ADDRESS = "0xca143Ce32Fe78f1f7019d7d551a6402fC5350c73"

# =========================
# Observation Parameters
# =========================

# Observation interval in seconds
# (e.g. 300 = 5 min, 900 = 15 min, 3600 = 1 hr)
OBSERVATION_INTERVAL = 900

# =========================
# Data Storage
# =========================

# Base directory for data output
DATA_DIR = "data"

# CSV log file (single-asset initially)
LEM_LOG_FILE = "data/lem_observations.csv"

# =========================
# External Price Source
# =========================

# CoinGecko API endpoint for native asset price
COINGECKO_NATIVE_PRICE_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=binancecoin&vs_currencies=usd"
)

# =========================
# Research Mode Flags
# =========================

# This system is read-only by design
READ_ONLY_MODE = True