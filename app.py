import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da página ---
#Definir o título da página, o ícone e o layout para ocupar a largura inteira
#slario na area de dados
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="🐼",
    layout="wide",
)

# Carregamento dos dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra lateral - filtros
st.sidebar.header("🔍Filtros")

# Filtro de Ano
anos_dispo = sorted(df['ano'].unique())
anos_select = st.sidebar.multiselect('Ano', anos_dispo, default=anos_dispo)

# Filtro de Senioridade
senioridades_dispo = sorted(df['senioridade'].unique())
senioridades_select = st.sidebar.multiselect('Senioridade', senioridades_dispo, default=senioridades_dispo)

# Tipo de Contrato
contratos_dispo = sorted(df['contrato'].unique())
contratos_select = st.sidebar.multiselect('Tipo de Contrato', contratos_dispo, default=contratos_dispo)

# Filtro por Tamanho Empresa
tamanhos_dispo = sorted(df['tamanho_empresa'].unique())
tamanhos_select = st.sidebar.multiselect('Tamanho da Empresa', tamanhos_dispo, default=tamanhos_dispo)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[ #Filtar as escolhas do usuário
    (df['ano'].isin(anos_select)) &
    (df['senioridade'].isin(senioridades_select)) &
    (df['contrato'].isin(contratos_select)) &
    (df['tamanho_empresa'].isin(tamanhos_select))
]

# --- Conteúdo Principal ---
# Criação de uma seção para exibir o gráfico
st.header("📊 Gráfico de Salários")
st.markdown('Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.')
#st.write(df_filtrado.head()) # Mostrar as primeiras linhas do dataframe.

# --- Métricas Principais (KPIs) ---
st.subheader('Métricas gerais (Salário anual em USD)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0] #Shape
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
    #st.write(f'Salário médio: ${salario_medio:.2f}')
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ''
    st.write('Nenhum registro encontrado')

#Colunas
col1, col2, col3, col4 = st.columns(4)
col1.metric('Salário médio: ', f'${salario_medio:,.0f}')
col2.metric('Salário máximo: ', f'${salario_maximo:,.0f}')
col3.metric('Total de Registros:', f'{total_registros:,}')
col4.metric('Cargo mais frequente', cargo_mais_frequente)

st.markdown('---')

# --- Análises Visuais com Plotly ---
# Criação de uma seção para exibir o gráfico
st.subheader('Gráficos')
#st.write(df_filtrado.head()) # Mostrar as primeiras linhas do dataframe.
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargo = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargo = px.bar(
            top_cargo,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 cargos por salário médio',
            labels={'usd': 'Salário médio anual (USD)', 'cargo': 'Cargo'},
        )
        grafico_cargo.update_layout(title_x=0.1,yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargo, use_container_width=True)
    else:
        st.warning('Nenhum dados para exibir no gráfico de cargos.')

with col_graf2:
    if not df_filtrado.empty:
            grafico_hist = px.histogram(
            df_filtrado, 
            x='usd', 
            nbins=30, 
            title='Distribuição de Salários',
            labels={'usd': 'Salário anual (USD)', 'count': ''},
        )
            grafico_hist.update_layout(title_x=0.1)
            st.plotly_chart(grafico_hist, use_container_width=True)
#linha de baixo
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem, 
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos Tipos de trabalho',
            #hole=0.5
            )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dados para exibir no gráfico de tipos de trabalho.')

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='Blues',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)