import streamlit as st
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

st.title("📉 Indicadores")

ativo = st.selectbox(
    "Ativo",
    ["BTC-USD", "ETH-USD", "EURUSD=X"]
)

df = yf.download(
    ativo,
    period="60d",
    interval="1h",
    progress=False
)

close = df["Close"].squeeze()

df["RSI"] = RSIIndicator(
    close=close,
    window=14
).rsi()

df["EMA9"] = EMAIndicator(
    close=close,
    window=9
).ema_indicator()

df["EMA21"] = EMAIndicator(
    close=close,
    window=21
).ema_indicator()

st.dataframe(
    df[
        ["Close", "RSI", "EMA9", "EMA21"]
    ].tail(20)
)
