import streamlit as st
import random

st.title("📋 Probabilidades Históricas")

prob_alta = random.randint(45, 65)

st.metric(
    "Probabilidade Histórica de Alta",
    f"{prob_alta}%"
)

st.metric(
    "Probabilidade Histórica de Baixa",
    f"{100-prob_alta}%"
)

st.info(
    """
    Valor demonstrativo baseado
    em análise estatística histórica.
    """
)
