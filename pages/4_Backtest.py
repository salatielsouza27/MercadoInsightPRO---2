import streamlit as st
import yfinance as yf

st.title("📊 Backtest")

df = yf.download(
    "BTC-USD",
    period="180d",
    interval="1h",
    progress=False
)

df["retorno"] = df["Close"].pct_change()

st.metric(
    "Retorno Médio",
    f"{df['retorno'].mean()*100:.2f}%"
)

st.line_chart(df["Close"])
