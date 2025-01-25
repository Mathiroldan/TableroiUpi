import pandas as pd
import streamlit as st

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Financiero", page_icon=":bar_chart:", layout="wide")

# Inserción del logo de la empresa
st.image("Logo iUpi.png", width=200)  # Asegúrate de tener un archivo 'logo.png' en la misma carpeta que este script

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

# Desglose por perfil de inversión
st.subheader("Distribución por Perfil de Inversión")
perfil_distribucion = usuarios_activos['perfil'].value_counts()
st.bar_chart(perfil_distribucion)

# Desglose por instrumento
st.subheader("Distribución por Instrumento")
instrumento_distribucion = usuarios_activos['Instrumento'].value_counts()
st.bar_chart(instrumento_distribucion)

# Esconder "Hecho con Streamlit"
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
