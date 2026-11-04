import pandas as pd


def calculate_score(row):
    """
    Calcula uma pontuação de 0 a 100
    baseada em indicadores técnicos.
    """

    score = 0

    if row["EMA9"] > row["EMA21"]:
        score += 20

    if row["EMA21"] > row["EMA200"]:
        score += 20

    if row["RSI"] > 50:
        score += 20

    if row["MACD"] > row["MACD_SIGNAL"]:
        score += 20

    if row["Close"] > row["BB_MID"]:
        score += 20

    return score


def build_calibration_table(df, horizon=5):

    df = df.copy()

    df["future_return"] = (
        df["Close"].shift(-horizon)
        - df["Close"]
    )

    df["target"] = (
        df["future_return"] > 0
    ).astype(int)

    df["score"] = df.apply(
        calculate_score,
        axis=1
    )

    df["bucket"] = (
        df["score"] // 10
    ) * 10

    stats = (
        df.groupby("bucket")["target"]
        .mean()
        .reset_index()
    )

    stats["prob_up"] = (
        stats["target"] * 100
    )

    return stats


def get_probability(score, stats):

    bucket = (
        score // 10
    ) * 10

    result = stats[
        stats["bucket"] == bucket
    ]

    if result.empty:
        return 50.0

    return float(
        result["prob_up"].iloc[0]
    )
