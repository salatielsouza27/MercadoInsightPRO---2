import streamlit as st
from utils.yahoo_data import get_market_data

st.title("📊 Dashboard")

df = get_market_data(
    "BTC-USD",
    period="30d",
    interval="1h"
)

if df.empty:
    st.error("Sem dados disponíveis")
    st.stop()

close = df["Close"].squeeze()

ultimo = float(close.iloc[-1])

st.metric(
    "Preço Atual",
    f"${ultimo:,.2f}"
)

st.dataframe(df.tail())
