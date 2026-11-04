import pandas as pd

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands


def add_indicators(df):

    close = df["Close"]

    # RSI
    df["RSI"] = RSIIndicator(
        close=close,
        window=14
    ).rsi()

    # EMA
    df["EMA9"] = EMAIndicator(
        close=close,
        window=9
    ).ema_indicator()

    df["EMA21"] = EMAIndicator(
        close=close,
        window=21
    ).ema_indicator()

    df["EMA200"] = EMAIndicator(
        close=close,
        window=200
    ).ema_indicator()

    # MACD
    macd = MACD(close=close)

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    # Bollinger
    bb = BollingerBands(
        close=close,
        window=20,
        window_dev=2
    )

    df["BB_HIGH"] = bb.bollinger_hband()
    df["BB_MID"] = bb.bollinger_mavg()
    df["BB_LOW"] = bb.bollinger_lband()

    return df
