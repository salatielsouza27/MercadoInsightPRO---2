import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime
from zoneinfo import ZoneInfo

from ta.trend import EMAIndicator
from ta.volatility import BollingerBands

from utils.yahoo_data import get_market_data
from utils.indicators import add_indicators

from utils.probability_calibration import (
    calculate_score,
    build_calibration_table,
    get_probability
)

st.set_page_config(
    page_title="Gráficos",
    layout="wide"
)

st.title("📈 Gráfico Profissional")

# ==========================
# HORÁRIO BRASIL
# ==========================

agora = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.caption(
    f"Última atualização: {agora.strftime('%H:%M:%S')}"
)

# ==========================
# SELEÇÃO DE ATIVO
# ==========================

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

# ==========================
# DADOS
# ==========================

df = get_market_data(
    ativo,
    period="30d",
    interval="5m"
)

if df.empty:
    st.error("Sem dados disponíveis.")
    st.stop()

# Mantém últimos candles para melhor visualização

df = df.tail(150)

# ==========================
# INDICADORES
# ==========================

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
df["BB_MID"] = bb.bollinger_mavg()
df["BB_LOW"] = bb.bollinger_lband()

# ==========================
# PROBABILIDADE HISTÓRICA
# ==========================

try:

    df_prob = df.copy()

    df_prob["RSI"] = 50
    df_prob["MACD"] = 0
    df_prob["MACD_SIGNAL"] = 0

    stats = build_calibration_table(
        df_prob,
        horizon=3
    )

    current_score = calculate_score(
        df_prob.iloc[-1]
    )

    prob = get_probability(
        current_score,
        stats
    )

except Exception:

    prob = 50.0

if prob >= 60:

    tendencia = "📈 ALTA"
    cor = "#0f5132"

elif prob <= 40:

    tendencia = "📉 BAIXA"
    cor = "#842029"

else:

    tendencia = "➡️ NEUTRO"
    cor = "#664d03"

# ==========================
# GRÁFICO
# ==========================

fig = go.Figure()

# Candles

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
            width=2
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

# Layout

fig.update_layout(
    title=f"{ativo} - Timeframe 5 minutos",
    template="plotly_dark",
    height=850,
    hovermode="x unified",
    xaxis_rangeslider_visible=False
)

# ==========================
# CAIXA DE PROBABILIDADE
# ==========================

fig.add_annotation(
    x=0.80,
    y=0.95,

    xref="paper",
    yref="paper",

    showarrow=False,

    bgcolor=cor,

    bordercolor="white",
    borderwidth=1,

    opacity=0.90,

    align="left",

    font=dict(
        size=14,
        color="white"
    ),

    text=f"""
<b>{tendencia}</b><br>
Alta: {prob:.1f}%<br>
Baixa: {100-prob:.1f}%<br>
Horizonte: 15 min
"""
)

# ==========================
# EXIBIÇÃO
# ==========================

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# MÉTRICAS
# ==========================

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
