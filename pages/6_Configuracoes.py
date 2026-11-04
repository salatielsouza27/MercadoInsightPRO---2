import streamlit as st

st.title("⚙️ Configurações")

tema = st.selectbox(
    "Tema",
    ["Escuro", "Claro"]
)

ativo_padrao = st.selectbox(
    "Ativo Padrão",
    [
        "BTC-USD",
        "ETH-USD",
        "EURUSD=X"
    ]
)

st.success("Configurações salvas")
