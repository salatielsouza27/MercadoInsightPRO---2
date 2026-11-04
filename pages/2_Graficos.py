import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("📈 Gráficos")

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
    period="30d",
    interval="1h",
    progress=False
)

if df.empty:
    st.warning("Sem dados.")
    st.stop()

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )
    ]
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)
