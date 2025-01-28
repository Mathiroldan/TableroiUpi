import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Tipos y comportamiento de usuarios", page_icon=":bar_chart:", layout="wide")

# Inserción del logo de la empresa
st.image("images/Logo iUpi.png", width=200)  # Asegúrate de tener un archivo 'Logo iUpi.png'

# Carga de datos
data = pd.read_csv("data.csv")

# Asegurar que las fechas están en el formato correcto
data['fecha'] = pd.to_datetime(data['fecha'], format='%d/%m/%Y')

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtros disponibles
edad_filtro = st.sidebar.multiselect(
    "Selecciona Edad", 
    options=data['Edad'].unique(), 
    default=data['Edad'].unique()
)

perfil_filtro = st.sidebar.multiselect(
    "Selecciona Perfil", 
    options=data['perfil'].unique(), 
    default=data['perfil'].unique()
)

# Filtro por rango de fechas
min_date = data['fecha'].min()
max_date = data['fecha'].max()

fecha_inicio, fecha_fin = st.sidebar.date_input(
    "Selecciona un rango de fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Aplicar los filtros a todos los usuarios
usuarios_filtrados = data[
    (data['fecha'] >= pd.Timestamp(fecha_inicio)) &
    (data['fecha'] <= pd.Timestamp(fecha_fin)) &
    (data['Edad'].isin(edad_filtro)) & 
    (data['perfil'].isin(perfil_filtro))
]

# KPIs
st.title("Tipos y comportamientos de usuarios")

# KPI 1: Total de usuarios (incluye activos e inactivos)
total_usuarios = len(data)
st.metric("Usuarios Totales", total_usuarios)

# KPI 2: Total de usuarios activos
usuarios_activos = data[(data['monto ARS'] > 0) & (data['Instrumento'].notna())]
usuarios_activos_total = len(usuarios_activos)
st.metric("Usuarios Activos (que invirtieron alguna vez)", usuarios_activos_total)

# KPI 3: Monto total invertido por usuarios activos
monto_total_activos = usuarios_activos['monto ARS'].sum()
st.metric("Monto Total Activos (ARS)", f"${monto_total_activos:,.2f}")

# KPI 4: Promedio de monto invertido por usuario activo
promedio_monto_activos = usuarios_activos['monto ARS'].mean()
st.metric("Promedio Monto Activos (ARS)", f"${promedio_monto_activos:,.2f}")

# Gráfico de barra para franja etaria
st.subheader("Franja etaria de los usuarios")
# Definir el orden deseado para las franjas etarias
orden_edad = ['menos de 25 años', 'entre 26 y 35 años', 'entre 36 y 45 años', 'más de 46 años']
franja_etaria_distribucion = usuarios_filtrados['Edad'].value_counts().reindex(orden_edad).reset_index()
franja_etaria_distribucion.columns = ['Franja Etaria', 'Cantidad']

fig_bar_franja = px.bar(
    franja_etaria_distribucion, 
    x='Franja Etaria', 
    y='Cantidad',
    labels={'Cantidad': 'Número de Usuarios', 'Franja Etaria': 'Edad'}
)
st.plotly_chart(fig_bar_franja)

# Gráfico de barra para perfil financiero
st.subheader("Perfil financiero de los Usuarios")
# Definir el orden deseado para los perfiles
orden_perfil = ['conservador', 'moderado', 'agresivo']
perfil_distribucion = usuarios_filtrados['perfil'].value_counts().reindex(orden_perfil).reset_index()
perfil_distribucion.columns = ['Perfil', 'Cantidad']

fig_bar_perfil = px.bar(
    perfil_distribucion, 
    x='Perfil', 
    y='Cantidad',
    labels={'Cantidad': 'Número de Usuarios', 'Perfil': 'Perfil Financiero'}
)
st.plotly_chart(fig_bar_perfil)

# Gráfico de torta para la distribución por instrumento
st.subheader("Distribución por Instrumento")
instrumento_distribucion = usuarios_filtrados['Instrumento'].value_counts().reset_index()
instrumento_distribucion.columns = ['Instrumento', 'Cantidad']
fig_pie_instrumento = px.pie(
    instrumento_distribucion, 
    names='Instrumento', 
    values='Cantidad')
st.plotly_chart(fig_pie_instrumento)

# Gráfico de torta para objetivos
st.subheader("Objetivos de los Usuarios")
objetivos_distribucion = usuarios_filtrados['objetivo'].value_counts().reset_index()
objetivos_distribucion.columns = ['Objetivo', 'Cantidad']
fig_pie_objetivos = px.pie(
    objetivos_distribucion, 
    names='Objetivo', 
    values='Cantidad')
st.plotly_chart(fig_pie_objetivos)

# Gráfico de torta para razón de inversión
st.subheader("Razón de Inversión")
razon_distribucion = usuarios_filtrados['razon_inversion'].value_counts().reset_index()
razon_distribucion.columns = ['Razon', 'Cantidad']
fig_pie_razon = px.pie(
    razon_distribucion, 
    names='Razon', 
    values='Cantidad')
st.plotly_chart(fig_pie_razon)

# Gráfico de línea para dinero invertido a lo largo del año
st.subheader("Dinero Invertido a lo Largo del Año")
dinero_por_mes = usuarios_filtrados.groupby(usuarios_filtrados['fecha'].dt.to_period('M'))['monto ARS'].sum().reset_index()
dinero_por_mes.columns = ['Mes', 'Monto Total']
dinero_por_mes['Mes'] = dinero_por_mes['Mes'].astype(str)
fig_line_dinero = px.line(
    dinero_por_mes, 
    x='Mes', 
    y='Monto Total')
st.plotly_chart(fig_line_dinero)

# Esconder "Hecho con Streamlit"
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
