import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da página ---
#Definir o título da página, o ícone e o layout para ocupar a largura inteira
#slario na area de dados
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon=":chart_with_upwards_trend:📈🐼",
    layout="wide",
)

# Carregamento dos dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra lateral - filtros
st.sidebar.header("🔍Filtros")

# Filtro de Ano
