import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Desafio Indicium",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    conn = sqlite3.connect("raw_data.db")

    orders = pd.read_sql("SELECT * FROM orders", conn)
    customers = pd.read_sql("SELECT * FROM customers", conn)

    conn.close()

    return orders, customers

orders, customers = carregar_dados()

st.title("🚤 Desafio Indicium 2026")
st.markdown("Análise de vendas da Nautilus")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pedidos", f"{len(orders):,}")

with col2:
    st.metric("Clientes", f"{customers['id'].nunique():,}")

with col3:
    st.metric(
        "Faturamento",
        f"R$ {orders['total'].sum():,.2f}"
    )

orders['created_at'] = pd.to_datetime(
    orders['created_at']
)

vendas_mes = (
    orders
    .groupby(
        orders['created_at'].dt.to_period('M')
    )['total']
    .sum()
    .reset_index()
)

vendas_mes['created_at'] = (
    vendas_mes['created_at']
    .astype(str)
)

fig = px.line(
    vendas_mes,
    x='created_at',
    y='total',
    title='Faturamento Mensal'
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.header("📊 Principais Resultados")

st.success("""
✅ Melhor Coorte: Janeiro/2020

✅ MRR após 12 meses:
R$ 5.045.974,74

✅ Produto mais similar ao
Motor de Popa 1949:
Motor de Popa 5331

✅ Forecast Q1/2026:
81 unidades

✅ Pior dia da semana:
Quinta-feira
""")
