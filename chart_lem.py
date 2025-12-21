"""
LEM v1.2 — Observation Charts (Provenance-Tolerant)
--------------------------------------------------
Read-only visualization of LEM behavior with mixed data sources.

Charts:
1) Token Price vs Liquidity Elasticity (LEM)
2) Market Cap vs Native Liquidity (LPₙ)

No signals. No thresholds. No interpretation.
"""

import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "data/lem_observations.csv"

# Select the pair you want to visualize
PAIR_ADDRESS = "0x933477eba23726ca95a957cb85dbb1957267ef85"


def load_data():
    df = pd.read_csv(CSV_FILE)

    # Parse timestamp safely
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce")

    # Ensure data_source column exists (legacy compatibility)
    if "data_source" not in df.columns:
        df["data_source"] = None

    # Filter by pair
    df = df[df["pair_address"] == PAIR_ADDRESS]

    # Drop rows with invalid timestamps or missing core values
    df = df.dropna(subset=[
        "timestamp_utc",
        "token_price_usd",
        "lem",
        "market_cap_usd",
        "lp_native_usd",
    ])

    # Sort chronologically
    df = df.sort_values("timestamp_utc")

    return df


def plot_price_vs_lem(df):
    fig, ax_price = plt.subplots(figsize=(12, 6))

    ax_price.set_title("Token Price vs Liquidity Elasticity (LEM)")
    ax_price.set_xlabel("Date (UTC)")
    ax_price.set_ylabel("Token Price (USD)")
    ax_price.set_yscale("log")

    ax_price.plot(
        df["timestamp_utc"],
        df["token_price_usd"],
        label="Token Price (USD)",
    )

    ax_lem = ax_price.twinx()
    ax_lem.set_ylabel("LEM")

    ax_lem.plot(
        df["timestamp_utc"],
        df["lem"],
        label="LEM",
        linestyle="--",
    )

    fig.legend(loc="upper left")
    plt.tight_layout()
    plt.show()


def plot_mc_lp(df):
    plt.figure(figsize=(12, 6))
    plt.title("Market Cap vs Native Liquidity (LPₙ)")
    plt.xlabel("Date (UTC)")
    plt.ylabel("USD")

    plt.plot(
        df["timestamp_utc"],
        df["market_cap_usd"],
        label="Market Cap (USD)",
    )

    plt.plot(
        df["timestamp_utc"],
        df["lp_native_usd"],
        label="Native Liquidity LPₙ (USD)",
    )

    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = load_data()

    if data.empty:
        raise ValueError(
            f"No valid data found for pair {PAIR_ADDRESS}. "
            "Check that the pair_address exists in the CSV."
        )

    plot_price_vs_lem(data)
    plot_mc_lp(data)