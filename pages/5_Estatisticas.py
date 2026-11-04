import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📊 Estatísticas")

df = yf.download(
    "BTC-USD",
    period="180d",
    interval="1d",
    auto_adjust=True,
    progress=False
)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    st.error("Sem dados disponíveis")
    st.stop()

retornos = df["Close"].pct_change().dropna()

volatilidade = float(retornos.std() * 100)
retorno_medio = float(retornos.mean() * 100)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Volatilidade",
        f"{volatilidade:.2f}%"
    )

with col2:
    st.metric(
        "Retorno Médio",
        f"{retorno_medio:.2f}%"
    )

st.line_chart(retornos)
st.dataframe(df.tail())
