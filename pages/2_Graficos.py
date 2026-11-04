import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.title("📈 Gráfico")

ativo = st.selectbox(
    "Selecione o ativo",
    [
        "BTC-USD",
        "ETH-USD",
        "EURUSD=X"
    ]
)

df = yf.download(
    ativo,
    period="5d",
    interval="1h",
    auto_adjust=True,
    progress=False
)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

st.write(df.tail())

if df.empty:
    st.error("Sem dados retornados")
    st.stop()

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )
)

fig.update_layout(
    template="plotly_dark",
    height=700,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)
