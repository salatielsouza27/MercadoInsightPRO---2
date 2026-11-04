import streamlit as st
import yfinance as yf

st.title("📈 Estatísticas")

df = yf.download(
    "BTC-USD",
    period="180d",
    interval="1d",
    progress=False
)

retornos = df["Close"].pct_change()

st.metric(
    "Volatilidade",
    f"{retornos.std()*100:.2f}%"
)

st.metric(
    "Retorno Médio",
    f"{retornos.mean()*100:.2f}%"
)

st.dataframe(df.tail())
