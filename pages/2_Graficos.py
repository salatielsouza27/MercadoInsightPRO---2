import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from ta.trend import EMAIndicator
from ta.volatility import BollingerBands

from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Gráficos",
    layout="wide"
)

st.title("📈 Gráfico Profissional")

agora = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.caption(
    f"Última atualização: {agora.strftime('%H:%M:%S')}"
)

ativo = st.selectbox(
    "Selecione o ativo",
    [
        "EURUSD=X",
        "GBPUSD=X",
        "USDJPY=X",
        "BTC-USD",
        "ETH-USD",
        "GC=F"
    ]
)

df = yf.download(
    ativo,
    period="1d",
    interval="5m",
    auto_adjust=True,
    progress=False,
    threads=False
)

# Corrige MultiIndex
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    st.error("Sem dados disponíveis.")
    st.stop()

# Mantém apenas últimos candles
df = df.tail(150)

close = df["Close"]

# ===== EMAs =====

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

# ===== BOLLINGER =====

bb = BollingerBands(
    close=close,
    window=20,
    window_dev=2
)

df["BB_HIGH"] = bb.bollinger_hband()
df["BB_MID"] = bb.bollinger_mavg()
df["BB_LOW"] = bb.bollinger_lband()

# ===== GRÁFICO =====

fig = go.Figure()

# Candlestick
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candles",

        increasing_line_color="lime",
        increasing_fillcolor="lime",

        decreasing_line_color="red",
        decreasing_fillcolor="red"
    )
)

# EMA 9
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA9"],
        name="EMA 9",
        line=dict(
            color="yellow",
            width=1
        )
    )
)

# EMA 21
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA21"],
        name="EMA 21",
        line=dict(
            color="cyan",
            width=2
        )
    )
)

# EMA 200
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA200"],
        name="EMA 200",
        line=dict(
            color="red",
            width=3
        )
    )
)

# Bollinger Superior
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_HIGH"],
        name="BB Superior",
        line=dict(
            color="green",
            width=1
        )
    )
)

# Bollinger Média
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_MID"],
        name="BB Média",
        line=dict(
            color="white",
            width=1
        )
    )
)

# Bollinger Inferior
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_LOW"],
        name="BB Inferior",
        line=dict(
            color="green",
            width=1
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    height=850,
    hovermode="x unified",
    xaxis_rangeslider_visible=False,
    title=f"{ativo} - Timeframe 5 minutos"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===== MÉTRICAS =====

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Preço Atual",
        f"{float(df['Close'].iloc[-1]):.5f}"
    )

with col2:
    st.metric(
        "Máxima",
        f"{float(df['High'].max()):.5f}"
    )

with col3:
    st.metric(
        "Mínima",
        f"{float(df['Low'].min()):.5f}"
    )

st.subheader("Últimos Registros")

st.dataframe(
    df.tail(10),
    use_container_width=True
)
