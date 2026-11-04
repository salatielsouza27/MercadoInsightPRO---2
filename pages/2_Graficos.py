import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from ta.trend import EMAIndicator
from ta.volatility import BollingerBands

from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.set_page_config(layout="wide")

st.title("📈 Gráfico Profissional")

# Atualiza automaticamente a cada 10 segundos
st_autorefresh(
    interval=10000,
    key="grafico_refresh"
)

st.caption(
    f"Última atualização: {datetime.now().strftime('%H:%M:%S')}"
)

ativo = st.selectbox(
    "Selecione o ativo",
    [
        "BTC-USD",
        "ETH-USD",
        "EURUSD=X",
        "GBPUSD=X",
        "USDJPY=X",
        "GC=F"
    ]
)

df = yf.download(
    ativo,
    period="1d",
    interval="1m",
    auto_adjust=True,
    progress=False,
    threads=False
)

# Corrige MultiIndex do yfinance
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    st.error("Sem dados disponíveis.")
    st.stop()

# Indicadores
close = df["Close"]

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

bb = BollingerBands(
    close=close,
    window=20,
    window_dev=2
)

df["BB_HIGH"] = bb.bollinger_hband()
df["BB_LOW"] = bb.bollinger_lband()
df["BB_MID"] = bb.bollinger_mavg()

# Gráfico
fig = go.Figure()

# Candles
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

# EMA 9
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA9"],
        mode="lines",
        name="EMA 9",
        line=dict(color="yellow", width=1)
    )
)

# EMA 21
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA21"],
        mode="lines",
        name="EMA 21",
        line=dict(color="cyan", width=2)
    )
)

# EMA 200
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA200"],
        mode="lines",
        name="EMA 200",
        line=dict(color="red", width=2)
    )
)

# Bollinger Superior
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_HIGH"],
        mode="lines",
        name="BB Superior",
        line=dict(color="green")
    )
)

# Bollinger Média
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_MID"],
        mode="lines",
        name="BB Média",
        line=dict(color="white")
    )
)

# Bollinger Inferior
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_LOW"],
        mode="lines",
        name="BB Inferior",
        line=dict(color="green")
    )
)

fig.update_layout(
    title=f"{ativo}",
    template="plotly_dark",
    height=800,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Informações adicionais
col1, col2, col3 = st.columns(3)

ultimo = float(df["Close"].iloc[-1])

with col1:
    st.metric(
        "Preço Atual",
        f"{ultimo:.5f}"
    )

with col2:
    st.metric(
        "Máxima",
        f"{df['High'].iloc[-1]:.5f}"
    )

with col3:
    st.metric(
        "Mínima",
        f"{df['Low'].iloc[-1]:.5f}"
    )

st.subheader("Últimos Registros")

st.dataframe(
    df.tail(10),
    use_container_width=True
)
