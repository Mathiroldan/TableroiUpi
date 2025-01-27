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

st.write("Valores reales en Edad:", usuarios_activos['Edad'].unique())
st.write("Valores reales en Perfil:", usuarios_activos['perfil'].unique())
st.write("Valores reales en Trimestre:", usuarios_activos['Trimestre'].unique())

# KPI 3: Monto total invertido por usuarios activos
monto_total_activos = usuarios_activos['monto ARS'].sum()
st.metric("Monto Total Activos (ARS)", f"${monto_total_activos:,.2f}")

# KPI 4: Promedio de monto invertido por usuario activo
promedio_monto_activos = usuarios_activos['monto ARS'].mean()
st.metric("Promedio Monto Activos (ARS)", f"${promedio_monto_activos:,.2f}")

# Asegurar que las fechas están en el formato correcto
usuarios_activos['fecha'] = pd.to_datetime(usuarios_activos['fecha'], format='%d/%m/%Y')

# Agregar columna de trimestres
usuarios_activos['Trimestre'] = usuarios_activos['fecha'].dt.to_period('Q').astype(str)

#Corregir lectura de trimestres
usuarios_activos['Trimestre'] = usuarios_activos['Trimestre'].str[-2:]

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtros disponibles
edad_filtro = st.sidebar.multiselect(
    "Selecciona Edad", 
    options=list(usuarios_activos['Edad'].unique()), 
    default=list(usuarios_activos['Edad'].unique())
)

perfil_filtro = st.sidebar.multiselect(
    "Selecciona Perfil", 
    options=list(usuarios_activos['perfil'].unique()), 
    default=list(usuarios_activos['perfil'].unique())
)

trimestre_filtro = st.sidebar.multiselect(
    "Selecciona Trimestre", 
    options=list(usuarios_activos['Trimestre'].unique()), 
    default=list(usuarios_activos['Trimestre'].unique())
)

# Aplicar los filtros
usuarios_filtrados = usuarios_activos[
    (usuarios_activos['Edad'].isin(edad_filtro)) & 
    (usuarios_activos['perfil'].isin(perfil_filtro)) & 
    (usuarios_activos['Trimestre'].isin(trimestre_filtro))
]

# Gráfico de torta para la distribución por instrumento
st.subheader("Distribución por Instrumento")
instrumento_distribucion = usuarios_activos['Instrumento'].value_counts().reset_index()
instrumento_distribucion.columns = ['Instrumento', 'Cantidad']
fig_pie_instrumento = px.pie(
    instrumento_distribucion, 
    names='Instrumento', 
    values='Cantidad', 
    title="Distribución por Instrumento")
st.plotly_chart(fig_pie_instrumento)

# Gráfico de torta para objetivos
st.subheader("Objetivos de los Usuarios")
objetivos_distribucion = usuarios_activos['objetivo'].value_counts().reset_index()
objetivos_distribucion.columns = ['Objetivo', 'Cantidad']
fig_pie_objetivos = px.pie(
    objetivos_distribucion, 
    names='Objetivo', 
    values='Cantidad', 
    title="Distribución de Objetivos")
st.plotly_chart(fig_pie_objetivos)

# Gráfico de torta para razón de inversión
st.subheader("Razón de Inversión")
razon_distribucion = usuarios_activos['razon_inversion'].value_counts().reset_index()
razon_distribucion.columns = ['Razon', 'Cantidad']
fig_pie_razon = px.pie(
    razon_distribucion, 
    names='Razon', 
    values='Cantidad', 
    title="Razón de Inversión")
st.plotly_chart(fig_pie_razon)

# Gráfico de barra para franja etaria
st.subheader("Franja Etaria de los Usuarios")
franja_etaria_distribucion = usuarios_activos['Edad'].value_counts().reset_index()
franja_etaria_distribucion.columns = ['Franja Etaria', 'Cantidad']
fig_bar_franja = px.bar(
    franja_etaria_distribucion, 
    x='Franja Etaria', 
    y='Cantidad', 
    title="Franja Etaria de los Usuarios")
st.plotly_chart(fig_bar_franja)

# Gráfico de línea para dinero invertido a lo largo del año
st.subheader("Dinero Invertido a lo Largo del Año")
dinero_por_mes = usuarios_activos.groupby(usuarios_activos['fecha'].dt.to_period('M'))['monto ARS'].sum().reset_index()
dinero_por_mes.columns = ['Mes', 'Monto Total']
dinero_por_mes['Mes'] = dinero_por_mes['Mes'].astype(str)
fig_line_dinero = px.line(
    dinero_por_mes, 
    x='Mes', 
    y='Monto Total', 
    title="Dinero Invertido a lo Largo del Año")
st.plotly_chart(fig_line_dinero)

# Mensaje final
st.write("### Datos filtrados")
st.dataframe(usuarios_activos)

# Esconder "Hecho con Streamlit"
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
