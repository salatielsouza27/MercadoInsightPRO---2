import streamlit as st
import yfinance as yf

st.title("📊 Dashboard")

ativo = "BTC-USD"

df = yf.download(
    ativo,
    period="5d",
    interval="1h",
    progress=False
)

ultimo = float(df["Close"].iloc[-1])

st.metric(
    "Preço Atual",
    f"${ultimo:,.2f}"
)

st.dataframe(df.tail(10))
