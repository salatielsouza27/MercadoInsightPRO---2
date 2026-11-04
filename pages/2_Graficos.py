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
        "EURUSD=X",
        "GBPUSD=X"
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

if df.empty:
    st.error("Sem dados disponíveis.")
    st.stop()

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candles"
    )
)

fig.update_layout(
    title=f"{ativo}",
    template="plotly_dark",
    height=700,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Últimos registros")

st.dataframe(df.tail())
from streamlit_autorefresh import st_autorefresh
st_autorefresh(
    interval=60000,  # 60 segundos
    key="refresh_grafico"
)
from ta.trend import EMAIndicator
close = df["Close"]

df["EMA9"] = EMAIndicator(
    close=close,
    window=9
).ema_indicator()

df["EMA21"] = EMAIndicator(
    close=close,
    window=21
).ema_indicator()
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA9"],
        name="EMA 9",
        line=dict(color="yellow")
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA21"],
        name="EMA 21",
        line=dict(color="cyan")
    )
)
