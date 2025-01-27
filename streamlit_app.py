import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Financiero", page_icon=":bar_chart:", layout="wide")

# Inserción del logo de la empresa
st.image("images/Logo iUpi.png", width=200)  # Asegúrate de tener un archivo 'Logo iUpi.png'

# Carga de datos
data = pd.read_csv("data.csv")

# Filtrar datos con montos mayores a 0 y eliminar filas con columna 'Instrumento' vacía
usuarios_activos = data[(data['monto ARS'] > 0) & (data['Instrumento'].notna())]

# KPIs
st.title("Dashboard Financiero")

# KPI 1: Total de usuarios (incluye activos e inactivos)
total_usuarios = len(data)
st.metric("Usuarios Totales", total_usuarios)

# KPI 2: Total de usuarios activos
usuarios_activos_total = len(usuarios_activos)
st.metric("Usuarios Activos", usuarios_activos_total)

# KPI 3: Monto total invertido por usuarios activos
monto_total_activos = usuarios_activos['monto ARS'].sum()
st.metric("Monto Total Activos (ARS)", f"${monto_total_activos:,.2f}")

# KPI 4: Promedio de monto invertido por usuario activo
promedio_monto_activos = usuarios_activos['monto ARS'].mean()
st.metric("Promedio Monto Activos (ARS)", f"${promedio_monto_activos:,.2f}")

# Filtros por edad, perfil y trimestre
st.sidebar.title("Filtros")
edad_filtro = st.sidebar.multiselect("Selecciona franja etaria:", data['Edad'].unique())
perfil_filtro = st.sidebar.multiselect("Selecciona perfil:", data['perfil'].unique())
trimestre_filtro = st.sidebar.multiselect("Selecciona trimestre:", ["Q1", "Q2", "Q3", "Q4"])

# Aplicar filtros
if edad_filtro:
    data = data[data['Edad'].isin(edad_filtro)]
if perfil_filtro:
    data = data[data['perfil'].isin(perfil_filtro)]
if trimestre_filtro:
    data['trimestre'] = pd.to_datetime(data['fecha']).dt.quarter
    data = data[data['trimestre'].isin([int(q[-1]) for q in trimestre_filtro])]

# Gráficos
# 1. Gráfico Treemap o de Torta: Distribución por Instrumento Financiero
st.subheader("Distribución por Instrumento Financiero")
instrumento_distribucion = usuarios_activos['Instrumento'].value_counts()
try:
    fig_treemap = px.treemap(instrumento_distribucion.reset_index(), path=['index'], values='Instrumento')
    st.plotly_chart(fig_treemap)
except Exception:
    fig_pie = px.pie(instrumento_distribucion.reset_index(), names='index', values='Instrumento')
    st.plotly_chart(fig_pie)

# 2. Gráfico de Torta: Objetivos de los Usuarios
st.subheader("Objetivos de los Usuarios")
objetivos_distribucion = usuarios_activos['objetivo'].value_counts()
fig_objetivos = px.pie(objetivos_distribucion.reset_index(), names='index', values='objetivo')
st.plotly_chart(fig_objetivos)

# 3. Gráfico de Torta: Razón de Inversión
st.subheader("Razón de Inversión")
razon_inversion_distribucion = usuarios_activos['razon_inversion'].value_counts()
fig_razon = px.pie(razon_inversion_distribucion.reset_index(), names='index', values='razon_inversion')
st.plotly_chart(fig_razon)

# 4. Gráfico de Barras: Franja Etaria
st.subheader("Franja Etaria de los Usuarios")
franja_etaria_distribucion = usuarios_activos['Edad'].value_counts().sort_index()
fig_franja = px.bar(franja_etaria_distribucion.reset_index(), x='index', y='Edad', labels={'index': 'Franja Etaria', 'Edad': 'Cantidad de Usuarios'})
st.plotly_chart(fig_franja)

# 5. Gráfico de Línea: Dinero Invertido a lo Largo del Año
st.subheader("Dinero Invertido a lo Largo del Año")
usuarios_activos['fecha'] = pd.to_datetime(usuarios_activos['fecha'])
usuarios_activos['mes'] = usuarios_activos['fecha'].dt.to_period('M').astype(str)
dinero_mensual = usuarios_activos.groupby('mes')['monto ARS'].sum().reset_index()
fig_linea = px.line(dinero_mensual, x='mes', y='monto ARS', labels={'mes': 'Mes', 'monto ARS': 'Monto Total (ARS)'})
st.plotly_chart(fig_linea)

# Esconder "Hecho con Streamlit"
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
