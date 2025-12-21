"""
LEM v1.0 — Blockchain Interface Layer
------------------------------------
This module handles all direct blockchain interactions.
It contains NO financial logic and NO calculations.

Responsibilities:
- Connect to RPC
- Instantiate contracts
- Read raw on-chain values
- Normalize decimals

All values returned are Python-native types.
"""

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
from config import RPC_URL
from abi import PAIR_ABI, ERC20_ABI


# =========================
# Web3 Initialization
# =========================

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise ConnectionError("Failed to connect to RPC endpoint")


# =========================
# Contract Helpers
# =========================

def get_contract(address: str, abi: list):
    """
    Instantiate a contract object.
    """
    return w3.eth.contract(
        address=Web3.to_checksum_address(address),
        abi=abi
    )


# =========================
# Pair-Level Reads
# =========================

def get_pair_reserves(pair_address: str) -> dict:
    """
    Fetch reserves from an AMM pair contract.

    Returns:
        {
            "reserve0": float,
            "reserve1": float,
            "timestamp": int
        }
    """
    pair = get_contract(pair_address, PAIR_ABI)

    try:
        reserve0, reserve1, timestamp = pair.functions.getReserves().call()
    except BadFunctionCallOutput:
        raise ValueError("Invalid pair address or ABI mismatch")

    return {
        "reserve0": reserve0,
        "reserve1": reserve1,
        "timestamp": timestamp
    }


def get_pair_tokens(pair_address: str) -> dict:
    """
    Fetch token0 and token1 addresses from a pair contract.

    Returns:
        {
            "token0": str,
            "token1": str
        }
    """
    pair = get_contract(pair_address, PAIR_ABI)

    token0 = pair.functions.token0().call()
    token1 = pair.functions.token1().call()

    return {
        "token0": Web3.to_checksum_address(token0),
        "token1": Web3.to_checksum_address(token1)
    }


# =========================
# Token-Level Reads
# =========================

def get_token_decimals(token_address: str) -> int:
    """
    Fetch decimals for an ERC-20 token.
    """
    token = get_contract(token_address, ERC20_ABI)

    try:
        return token.functions.decimals().call()
    except BadFunctionCallOutput:
        raise ValueError("Invalid token address or ABI mismatch")


def get_total_supply(token_address: str) -> float:
    """
    Fetch and normalize total token supply.
    """
    token = get_contract(token_address, ERC20_ABI)

    raw_supply = token.functions.totalSupply().call()
    decimals = get_token_decimals(token_address)

    return raw_supply / (10 ** decimals)


# =========================
# Normalization Utilities
# =========================

def normalize_reserve(raw_reserve: int, decimals: int) -> float:
    """
    Normalize raw reserve values using token decimals.
    """
    return raw_reserve / (10 ** decimals)