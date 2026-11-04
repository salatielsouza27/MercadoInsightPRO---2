import streamlit as st

from utils.yahoo_data import get_market_data
from utils.indicators import add_indicators

from utils.probability_calibration import (
    calculate_score,
    build_calibration_table,
    get_probability
)

st.title("📊 Probabilidades Históricas")

ATIVO = "EURUSD=X"

df = get_market_data(
    ATIVO,
    period="30d",
    interval="5m"
)

if df.empty:
    st.error("Sem dados disponíveis")
    st.stop()

df = add_indicators(df)

stats = build_calibration_table(
    df,
    horizon=3
)

current_score = calculate_score(
    df.iloc[-1]
)

prob = get_probability(
    current_score,
    stats
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Probabilidade Histórica de Alta",
        f"{prob:.1f}%"
    )

with col2:
    st.metric(
        "Probabilidade Histórica de Baixa",
        f"{100-prob:.1f}%"
    )

st.progress(
    prob / 100
)

st.write("---")

st.write("Ativo:", ATIVO)

st.write(
    "Timeframe:",
    "5 minutos"
)

st.write(
    "Horizonte:",
    "15 minutos (3 candles)"
)

st.write(
    "Registros analisados:",
    len(df)
)

st.dataframe(
    stats,
    use_container_width=True
)
