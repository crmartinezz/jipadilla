import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Configuración inicial del Dashboard
st.set_page_config(page_title='Dashboard Agroindustria', layout='wide')

# Sidebar para navegación
st.sidebar.title("📌 Navegación")
page = st.sidebar.radio("Seleccionar Página", ["Generar Datos", "Cargar CSV"])

if page == "Generar Datos":
    # Función para generar datos aleatorios de agroindustria
    def generar_datos(filas):
        cultivos = ['Maíz', 'Trigo', 'Arroz', 'Café', 'Caña de Azúcar', 'Soja', 'Papa', 'Frutas', 'Verduras']
        precios_base = np.random.uniform(50, 500, size=len(cultivos))
        
        data = []
        for i in range(filas):
            cultivo = np.random.choice(cultivos)
            precio = precios_base[list(cultivos).index(cultivo)] + np.random.uniform(-20, 20)
            tiempo = pd.Timestamp('2025-01-01') + pd.to_timedelta(i, unit='D')
            produccion = np.random.randint(100, 10000)
            
            data.append([cultivo, tiempo, precio, produccion])
        
        df = pd.DataFrame(data, columns=['Cultivo', 'Fecha', 'Precio', 'Producción'])
        return df
    
    # Parámetros en la barra lateral
    total_filas = st.sidebar.slider("Número de filas", min_value=50, max_value=1000, value=200, step=50)
    
    # Generación de datos
    df = generar_datos(total_filas)
    
    # Mostrar la tabla de datos
    st.subheader("📊 Datos Generados")
    st.dataframe(df)
    
    # Gráficos interactivos
    st.subheader("📈 Visualización de Datos")
    grafico_tipo = st.selectbox("Seleccionar tipo de gráfico", ['Línea', 'Barras', 'Dispersión'])
    
    if grafico_tipo == 'Línea':
        fig = px.line(df, x='Fecha', y='Precio', color='Cultivo', title='Evolución del Precio en el Tiempo')
    elif grafico_tipo == 'Barras':
        fig = px.bar(df, x='Cultivo', y='Producción', title='Producción por Cultivo', color='Cultivo')
    elif grafico_tipo == 'Dispersión':
        fig = px.scatter(df, x='Producción', y='Precio', color='Cultivo', title='Relación entre Producción y Precio')
    
    st.plotly_chart(fig, use_container_width=True)

elif page == "Cargar CSV":
    st.subheader("📂 Cargar Archivo CSV")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        df_csv = pd.read_csv(uploaded_file)
        st.write("📋 Vista Previa de los Datos:")
        st.dataframe(df_csv)
        
        # Selección de columnas a graficar
        columnas_disponibles = df_csv.columns.tolist()
        columnas_seleccionadas = st.multiselect("Selecciona las columnas para graficar", columnas_disponibles)
        tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ['Línea', 'Barras', 'Dispersión', 'Pie', 'Histograma'])
        
        if columnas_seleccionadas:
            df_filtrado = df_csv[columnas_seleccionadas]
            
            # Verificar si son numéricas o categóricas
            if df_filtrado.select_dtypes(include=[np.number]).shape[1] == len(columnas_seleccionadas):
                # Variables numéricas
                if tipo_grafico == 'Línea':
                    fig = px.line(df_csv, x=columnas_seleccionadas[0], y=columnas_seleccionadas[1:], title='Gráfico de Línea')
                elif tipo_grafico == 'Barras':
                    fig = px.bar(df_csv, x=columnas_seleccionadas[0], y=columnas_seleccionadas[1:], title='Gráfico de Barras')
                elif tipo_grafico == 'Dispersión':
                    fig = px.scatter(df_csv, x=columnas_seleccionadas[0], y=columnas_seleccionadas[1:], title='Gráfico de Dispersión')
                elif tipo_grafico == 'Histograma':
                    fig = px.histogram(df_csv, x=columnas_seleccionadas[0], title='Histograma')
                
            else:
                # Variables categóricas - Conteo
                conteo = df_filtrado[columnas_seleccionadas[0]].value_counts().reset_index()
                conteo.columns = ['Categoría', 'Cantidad']
                
                if tipo_grafico == 'Barras':
                    fig = px.bar(conteo, x='Categoría', y='Cantidad', title='Conteo de Categorías')
                elif tipo_grafico == 'Pie':
                    fig = px.pie(conteo, names='Categoría', values='Cantidad', title='Distribución de Categorías')
                else:
                    st.warning("Las variables categóricas solo pueden graficarse en Barras o Pie.")
                    fig = None
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("Por favor, sube un archivo CSV para analizar los datos.")
    
# Botón de reinicio
if st.sidebar.button("🔄 Resetear Parámetros"):
    st.experimental_rerun()

st.success("Dashboard listo para análisis 🚀")
