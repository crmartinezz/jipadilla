
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import io

# Configuración inicial del Dashboard
st.set_page_config(page_title='Exploración de Streamlit', layout='wide')

st.title("🚀 Exploración de Streamlit: Funcionalidades Básicas")

st.write("En este dashboard exploraremos las funcionalidades clave de Streamlit para la carga y exportación de archivos, captura de imágenes y generación de datos.")

# Menú lateral para navegación
st.sidebar.title("📌 Menú de Opciones")
option = st.sidebar.radio("Selecciona una opción", ["Cargar Imagen", "Capturar Cámara", "Subir Archivo", "Generar Datos", "Configuraciones"])

# Opción 1: Cargar Imagen
def cargar_imagen():
    st.subheader("📸 Cargar una Imagen")
    imagen = st.file_uploader("Sube una imagen", type=['jpg', 'png', 'jpeg'])
    if imagen:
        st.image(Image.open(imagen), caption="Imagen Cargada", use_column_width=True)
        st.success("Imagen cargada exitosamente.")

# Opción 2: Capturar desde Cámara
def capturar_camara():
    st.subheader("📷 Capturar desde Cámara")
    imagen_capturada = st.camera_input("Captura una foto")
    if imagen_capturada:
        st.image(Image.open(imagen_capturada), caption="Imagen Capturada", use_column_width=True)
        st.success("Imagen capturada correctamente.")

# Opción 3: Cargar Archivo General
def cargar_archivo():
    st.subheader("📂 Cargar Archivo")
    archivo = st.file_uploader("Sube un archivo", type=['csv', 'txt', 'xlsx'])
    if archivo:
        st.success("Archivo subido correctamente.")
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
            st.dataframe(df)
        elif archivo.name.endswith(".xlsx"):
            df = pd.read_excel(archivo)
            st.dataframe(df)
        else:
            contenido = archivo.read().decode("utf-8")
            st.text_area("Contenido del Archivo", contenido, height=200)

# Opción 4: Generar Datos Internamente
def generar_datos():
    st.subheader("📊 Generación de Datos Aleatorios")
    num_filas = st.slider("Número de filas", 10, 100, 50)
    categorias = ['A', 'B', 'C', 'D']
    df = pd.DataFrame({
        'Categoría': np.random.choice(categorias, num_filas),
        'Valor': np.random.randint(10, 100, num_filas)
    })
    st.dataframe(df)
    grafico_tipo = st.selectbox("Seleccionar tipo de gráfico", ["Barras", "Pie", "Histograma"])
    if grafico_tipo == "Barras":
        fig = px.bar(df, x='Categoría', y='Valor', title='Gráfico de Barras')
    elif grafico_tipo == "Pie":
        fig = px.pie(df, names='Categoría', values='Valor', title='Gráfico de Pie')
    else:
        fig = px.histogram(df, x='Valor', title='Histograma de Valores')
    st.plotly_chart(fig, use_container_width=True)

# Opción 5: Configuraciones (Checklists y Radio Buttons)
def configuraciones():
    st.subheader("⚙️ Configuración y Preferencias")
    opciones_checklist = st.multiselect("Selecciona opciones de interés", ['Opción 1', 'Opción 2', 'Opción 3'])
    seleccion_radio = st.radio("Elige una preferencia", ['Preferencia A', 'Preferencia B', 'Preferencia C'])
    st.write(f"Has seleccionado las opciones: {opciones_checklist}")
    st.write(f"Has elegido: {seleccion_radio}")

# Ejecutar la opción seleccionada
if option == "Cargar Imagen":
    cargar_imagen()
elif option == "Capturar Cámara":
    capturar_camara()
elif option == "Subir Archivo":
    cargar_archivo()
elif option == "Generar Datos":
    generar_datos()
elif option == "Configuraciones":
    configuraciones()

st.success("Exploración de Streamlit finalizada. 🚀")
