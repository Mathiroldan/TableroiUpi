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
# Filtros
st.sidebar.header("Filtros")

# Filtrar por edad
edad_filtro = st.sidebar.multiselect("Selecciona Edad", options=usuarios_activos['Edad'].unique(), default=usuarios_activos['Edad'].unique())

# Filtrar por perfil
perfil_filtro = st.sidebar.multiselect("Selecciona Perfil", options=usuarios_activos['perfil'].unique(), default=usuarios_activos['perfil'].unique())

# Filtrar por trimestre
trimestre_filtro = st.sidebar.multiselect(
    "Selecciona Trimestre", 
    options=usuarios_activos['Fecha'].dt.to_period('Q').unique(), 
    default=usuarios_activos['Fecha'].dt.to_period('Q').unique()
)

# Aplicar los filtros
usuarios_filtrados = usuarios_activos[
    (usuarios_activos['Edad'].isin(edad_filtro)) & 
    (usuarios_activos['perfil'].isin(perfil_filtro)) & 
    (usuarios_activos['Fecha'].dt.to_period('Q').isin(trimestre_filtro))
]

# Gráficos
# 1. Gráfico de Torta: Distribución por Instrumento Financiero
st.subheader("Distribución por Instrumento")

instrumento_distribucion = usuarios_activos['Instrumento'].value_counts().reset_index()
instrumento_distribucion.columns = ['Instrumento', 'Cantidad']  # Renombrar columnas

fig_pie = px.pie(instrumento_distribucion, names='Instrumento', values='Cantidad', title="Distribución por Instrumento")
st.plotly_chart(fig_pie)


# 2. Gráfico de Torta: Objetivos de los Usuarios
st.subheader("Objetivos de los Usuarios")

objetivos_distribucion = usuarios_activos['Objetivo'].value_counts().reset_index()
objetivos_distribucion.columns = ['Objetivo', 'Cantidad']

fig_objetivos = px.pie(objetivos_distribucion, names='Objetivo', values='Cantidad', title="Distribución de Objetivos")
st.plotly_chart(fig_objetivos)

# 3. Gráfico de Torta: Razón de Inversión
# Gráfico de torta para razón de inversión
st.subheader("Razón de Inversión")

razon_distribucion = usuarios_activos['Razon Inversion'].value_counts().reset_index()
razon_distribucion.columns = ['Razon', 'Cantidad']

fig_razon = px.pie(razon_distribucion, names='Razon', values='Cantidad', title="Razón de Inversión")
st.plotly_chart(fig_razon)

# 4. Gráfico de Barras: Franja Etaria
# Gráfico de barra para franja etaria
st.subheader("Franja Etaria de los Usuarios")

franja_etaria_distribucion = usuarios_activos['Edad'].value_counts().reset_index()
franja_etaria_distribucion.columns = ['Franja Etaria', 'Cantidad']

fig_franja_etaria = px.bar(franja_etaria_distribucion, x='Franja Etaria', y='Cantidad', title="Franja Etaria de los Usuarios")
st.plotly_chart(fig_franja_etaria)

# 5. Gráfico de Línea: Dinero Invertido a lo Largo del Año
# Gráfico de línea para dinero invertido a lo largo del año
st.subheader("Dinero Invertido a lo Largo del Año")

# Asegúrate de que las fechas estén en formato datetime
usuarios_activos['Fecha'] = pd.to_datetime(usuarios_activos['Fecha'], format='%d/%m/%Y')

# Agrupar por mes y sumar los montos
dinero_por_mes = usuarios_activos.groupby(usuarios_activos['Fecha'].dt.to_period('M'))['monto ARS'].sum().reset_index()
dinero_por_mes.columns = ['Mes', 'Monto Total']
dinero_por_mes['Mes'] = dinero_por_mes['Mes'].astype(str)  # Convertir a string para usar en gráficos

fig_dinero = px.line(dinero_por_mes, x='Mes', y='Monto Total', title="Dinero Invertido a lo Largo del Año")
st.plotly_chart(fig_dinero)

# Esconder "Hecho con Streamlit"
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
