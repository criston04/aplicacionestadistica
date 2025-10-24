"""
Aplicación principal de Análisis Estadístico Descriptivo v2.0
Autor: JOSE CAMARENA MEZA
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Importar módulos propios
from src.config import APP_CONFIG, FILE_CONFIG, CUSTOM_CSS
from src.utils import (
    determine_variable_type, 
    handle_missing_values,
    load_csv_file,
    load_excel_file,
    validate_dataframe,
    get_numeric_columns,
    get_categorical_columns,
    prepare_data_for_correlation,
    detect_and_convert_dates
)
from src.analysis import (
    calculate_frequency_table,
    calculate_all_measures_grouped,
    calculate_quartiles,
    calculate_correlation_matrix,
    detect_outliers_iqr,
    detect_outliers_zscore,
    test_normality,
    calculate_statistics_summary
)
from src.visualization import (
    apply_theme,
    generate_histogram,
    generate_interactive_histogram,
    generate_pie_chart,
    generate_bar_chart,
    generate_horizontal_bar_chart,
    generate_boxplot,
    generate_violinplot,
    generate_correlation_heatmap,
    generate_interactive_correlation_heatmap,
    generate_scatter_plot,
    generate_interactive_scatter,
    generate_qq_plot,
    generate_outliers_plot,
    generate_distribution_comparison
)
from src.export import (
    export_to_excel,
    export_to_pdf,
    generate_html_report,
    generate_r_code
)


def main():
    """Función principal de la aplicación."""
    
    # Configuración de la página
    st.set_page_config(
        page_title=APP_CONFIG['title'],
        page_icon=APP_CONFIG['icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
    )
    
    # Aplicar estilos CSS personalizados
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Título principal
    st.markdown('<p class="title">📊 Análisis Estadístico Descriptivo v2.0</p>', unsafe_allow_html=True)
    
    # Configuración de la barra lateral
    render_sidebar()
    
    # Contenido principal
    if st.session_state.get('uploaded_file') is not None:
        render_main_content()
    else:
        render_welcome_screen()
    
    # Footer
    st.markdown("""
        <div class="footer">
            Desarrollado por JOSE CAMARENA MEZA | Versión 2.0 | 2025
        </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Renderiza la barra lateral con opciones de configuración."""
    
    with st.sidebar:
        st.image("https://cdn.pixabay.com/photo/2018/09/18/11/19/business-3685935_960_720.png", width=100)
        st.markdown("### 📁 Carga de Datos")
        
        # Subir archivo
        uploaded_file = st.file_uploader(
            "Subir archivo", 
            type=FILE_CONFIG['allowed_extensions'],
            help="Soporta CSV, XLSX y TXT"
        )
        st.session_state['uploaded_file'] = uploaded_file
        
        if uploaded_file:
            st.success(f"✓ Archivo: {uploaded_file.name}")
        
        # Configuración de importación
        st.markdown("### ⚙️ Opciones de Importación")
        with st.expander("Configuración de archivo", expanded=False):
            separator = st.selectbox(
                "Separador", 
                FILE_CONFIG['separators'], 
                index=0,
                key="separator"
            )
            decimal = st.selectbox(
                "Separador decimal", 
                FILE_CONFIG['decimals'], 
                index=0,
                key="decimal"
            )
            encoding = st.selectbox(
                "Codificación", 
                FILE_CONFIG['encodings'], 
                index=0,
                key="encoding"
            )
        
        # Tema de visualización
        st.markdown("### 🎨 Personalización")
        theme = st.selectbox(
            "Tema de visualización", 
            ["default", "dark", "blue", "green", "purple"], 
            index=0,
            key="theme"
        )
        apply_theme(theme)
        
        # Información adicional
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; font-size: 0.8rem; color: #6c757d;">
                <b>Nuevas Funcionalidades v2.0:</b><br>
                ✓ Análisis de Correlación<br>
                ✓ Detección de Outliers<br>
                ✓ Pruebas de Normalidad<br>
                ✓ Gráficos Mejorados<br>
                ✓ UI Optimizada
            </div>
        """, unsafe_allow_html=True)


def render_welcome_screen():
    """Renderiza la pantalla de bienvenida."""
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://cdn.pixabay.com/photo/2018/09/18/11/19/business-3685935_960_720.png", width=150)
    
    with col2:
        st.markdown("""
        ## 🎯 Bienvenido a Análisis Estadístico v2.0
        
        Esta herramienta profesional te permite realizar análisis estadísticos avanzados:
        
        ### 📊 Características Principales:
        - **Análisis Descriptivo Completo**: Tablas de frecuencia, medidas de tendencia central y dispersión
        - **Análisis de Correlación**: Matrices de correlación con visualizaciones interactivas
        - **Detección de Outliers**: Métodos IQR y Z-score
        - **Pruebas de Normalidad**: Shapiro-Wilk, Kolmogorov-Smirnov, D'Agostino-Pearson
        - **Visualizaciones Avanzadas**: Gráficos interactivos con Plotly
        - **Exportación Múltiple**: Excel, PDF y HTML
        
        ### 🚀 Para comenzar:
        **Carga un archivo CSV, XLSX o TXT desde el panel lateral** ←
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tutorial rápido
    st.markdown('<p class="subtitle">📚 Tutorial Rápido</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "1️⃣ Cargar Datos", 
            "2️⃣ Análisis Básico", 
            "3️⃣ Análisis Avanzado",
            "4️⃣ Exportar"
        ])
        
        with tab1:
            st.markdown("""
            **Paso 1: Cargar tus datos**
            1. Usa el selector de archivos en la barra lateral
            2. Soporta CSV, XLSX y TXT (hasta 200 MB)
            3. Configura el separador y formato decimal si es necesario
            4. La aplicación validará y mostrará una vista previa
            """)
        
        with tab2:
            st.markdown("""
            **Paso 2: Análisis Descriptivo**
            1. Selecciona la columna a analizar
            2. La app detectará automáticamente el tipo de variable
            3. Maneja valores nulos según tus necesidades
            4. Obtén tablas de frecuencia y estadísticas
            """)
        
        with tab3:
            st.markdown("""
            **Paso 3: Análisis Avanzado (Nuevo en v2.0)**
            1. **Correlación**: Analiza relaciones entre múltiples variables
            2. **Outliers**: Detecta valores atípicos con IQR o Z-score
            3. **Normalidad**: Verifica si tus datos siguen distribución normal
            4. **Comparación**: Compara distribuciones visualmente
            """)
        
        with tab4:
            st.markdown("""
            **Paso 4: Exportar Resultados**
            1. Selecciona los componentes a incluir
            2. Elige el formato: Excel, PDF o HTML
            3. Descarga tu informe personalizado
            4. Comparte o archiva tus análisis
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_main_content():
    """Renderiza el contenido principal cuando hay datos cargados."""
    
    try:
        # Cargar datos
        uploaded_file = st.session_state['uploaded_file']
        
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
            df = load_csv_file(
                uploaded_file, 
                st.session_state.get('separator', ','),
                st.session_state.get('decimal', '.'),
                st.session_state.get('encoding', 'utf-8')
            )
        else:
            df = load_excel_file(uploaded_file)
        
        # Validar DataFrame
        is_valid, message = validate_dataframe(df)
        if not is_valid:
            st.error(f"❌ Error: {message}")
            return
        
        # Vista previa de datos
        st.markdown('<p class="subtitle">📋 Vista Previa de Datos</p>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Filas", f"{df.shape[0]:,}")
            with col2:
                st.metric("📈 Columnas", df.shape[1])
            with col3:
                st.metric("❌ Valores Nulos", f"{df.isna().sum().sum():,}")
            with col4:
                st.metric("💾 Tamaño", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabs principales para diferentes tipos de análisis
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Análisis Univariado",
            "🔗 Análisis de Correlación",
            "🎯 Detección de Outliers",
            "📐 Pruebas de Normalidad"
        ])
        
        with tab1:
            render_univariate_analysis(df)
        
        with tab2:
            render_correlation_analysis(df)
        
        with tab3:
            render_outlier_detection(df)
        
        with tab4:
            render_normality_tests(df)
        
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        st.exception(e)


def render_univariate_analysis(df):
    """Renderiza el análisis univariado."""
    
    st.markdown('<p class="subtitle">Análisis de Variable Única</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        selected_column = st.selectbox(
            "Seleccione la columna a analizar:",
            df.columns,
            key="univar_column"
        )
        
        column_dtype = df[selected_column].dtype
        st.info(f"💡 Tipo de datos detectado: **{column_dtype}**")
        
        # Manejo de valores nulos
        missing_values = df[selected_column].isna().sum()
        if missing_values > 0:
            st.warning(f"⚠️ La columna contiene **{missing_values:,}** valores nulos ({(missing_values/len(df)*100):.1f}%)")
            
            handle_missing = st.radio(
                "¿Cómo manejar los valores nulos?",
                ["Eliminar", "Reemplazar por la media", "Reemplazar por la mediana", "Reemplazar por cero"],
                key="handle_missing_univar"
            )
            
            df, msg = handle_missing_values(df, selected_column, handle_missing)
            st.success(msg)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis
    data = df[selected_column].dropna()
    variable_type = determine_variable_type(data)
    
    st.info(f"🔍 Tipo de variable detectado: **{variable_type}**")
    
    if st.button("🚀 Realizar Análisis Completo", key="analyze_univar", use_container_width=True):
        with st.spinner('⏳ Analizando datos...'):
            
            # Cálculo de tabla de frecuencia
            frequency_table = calculate_frequency_table(data, variable_type)
            
            # Medidas de resumen
            if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
                measures = calculate_all_measures_grouped(frequency_table)
            else:
                if variable_type == "Cuantitativa Discreta":
                    # Usar función mejorada para datos no agrupados
                    measures = calculate_statistics_summary(data)
                else:
                    mode_value = data.mode()[0] if not data.mode().empty else None
                    measures = {
                        'Moda': mode_value,
                        'Frecuencia de la Moda': data.value_counts().iloc[0] if not data.value_counts().empty else 0,
                        'Proporción de la Moda': round(data.value_counts().iloc[0] / len(data), 4) if not data.value_counts().empty else 0
                    }
            
            # Cuartiles
            quartiles = calculate_quartiles(data, frequency_table, variable_type)
            
            # Mostrar resultados
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📊 Tabla de Frecuencia")
                st.dataframe(pd.DataFrame(frequency_table), use_container_width=True, height=400)
            
            with col2:
                if measures:
                    st.markdown("### 📏 Medidas Estadísticas")
                    measures_df = pd.DataFrame(list(measures.items()), columns=['Medida', 'Valor'])
                    st.dataframe(measures_df, use_container_width=True, hide_index=True)
                
                if quartiles and any(v is not None for v in quartiles.values()):
                    st.markdown("### 📐 Cuartiles")
                    quartiles_df = pd.DataFrame(list(quartiles.items()), columns=['Cuartil', 'Valor'])
                    st.dataframe(quartiles_df, use_container_width=True, hide_index=True)
            
            # Visualizaciones
            st.markdown('<p class="subtitle">📈 Visualizaciones</p>', unsafe_allow_html=True)
            
            figs = []
            
            if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_hist = generate_histogram(data, variable_type, selected_column)
                    if fig_hist:
                        st.pyplot(fig_hist)
                        figs.append(fig_hist)
                
                with col2:
                    fig_box = generate_boxplot(data, variable_type, selected_column)
                    if fig_box:
                        st.pyplot(fig_box)
                        figs.append(fig_box)
                
                st.markdown("#### 🎯 Histograma Interactivo")
                fig_interactive = generate_interactive_histogram(data, variable_type, selected_column)
                if fig_interactive:
                    st.plotly_chart(fig_interactive, use_container_width=True)
                
                fig_violin = generate_violinplot(data, variable_type, selected_column)
                if fig_violin:
                    st.pyplot(fig_violin)
                    figs.append(fig_violin)
                    
            elif variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_bar = generate_bar_chart(data, variable_type, selected_column)
                    if fig_bar:
                        st.pyplot(fig_bar)
                        figs.append(fig_bar)
                
                with col2:
                    fig_pie = generate_pie_chart(data, variable_type, selected_column)
                    if fig_pie:
                        st.pyplot(fig_pie)
                        figs.append(fig_pie)
                
                fig_hbar = generate_horizontal_bar_chart(data, variable_type, selected_column)
                if fig_hbar:
                    st.pyplot(fig_hbar)
                    figs.append(fig_hbar)
            
            # Opciones de exportación
            render_export_section(df, selected_column, variable_type, frequency_table, measures, quartiles, figs)


def render_correlation_analysis(df):
    """Renderiza el análisis de correlación."""
    
    st.markdown('<p class="subtitle">Análisis de Correlación entre Variables</p>', unsafe_allow_html=True)
    
    # Información sobre conversión de fechas
    st.info("💡 **Tip:** Si tienes columnas con fechas (ej: 16/04/2024), se convertirán automáticamente a días transcurridos para poder calcular correlaciones.")
    
    # Preparar datos para correlación (convierte fechas automáticamente)
    df_prepared, conversion_info = prepare_data_for_correlation(df)
    
    # Mostrar información de conversiones si hay
    if conversion_info:
        with st.expander("ℹ️ Ver información de conversiones automáticas"):
            for col, info in conversion_info.items():
                if info['tipo_original'] == 'fecha':
                    st.write(f"**{col}**:")
                    st.write(f"  - Tipo original: Fecha")
                    st.write(f"  - Convertido a: Días transcurridos (0 = primera fecha)")
                    if 'info' in info and 'fecha_inicial' in info['info']:
                        st.write(f"  - Fecha inicial: {info['info']['fecha_inicial']}")
                        st.write(f"  - Fecha final: {info['info']['fecha_final']}")
                        st.write(f"  - Rango: {info['info']['rango_dias']} días")
    
    numeric_cols = list(df_prepared.columns)
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ Se necesitan al menos 2 variables numéricas (o fechas) para análisis de correlación.")
        return
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        selected_cols = st.multiselect(
            "Seleccione las variables para análisis de correlación:",
            numeric_cols,
            default=numeric_cols[:min(5, len(numeric_cols))],
            key="corr_columns"
        )
        
        if len(selected_cols) >= 2:
            if st.button("🔗 Calcular Matriz de Correlación", key="calc_corr", use_container_width=True):
                with st.spinner('Calculando correlaciones...'):
                    corr_matrix = calculate_correlation_matrix(df_prepared, selected_cols)
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("### 📊 Matriz de Correlación")
                        st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm', vmin=-1, vmax=1), use_container_width=True)
                    
                    with col2:
                        st.markdown("### 🎨 Mapa de Calor")
                        fig_heatmap = generate_correlation_heatmap(corr_matrix)
                        st.pyplot(fig_heatmap)
                    
                    st.markdown("### 🎯 Mapa de Calor Interactivo")
                    fig_interactive = generate_interactive_correlation_heatmap(corr_matrix)
                    st.plotly_chart(fig_interactive, use_container_width=True)
                    
                    # Pares de variables más correlacionadas
                    st.markdown("### 🔝 Correlaciones Más Fuertes")
                    corr_pairs = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_pairs.append({
                                'Variable 1': corr_matrix.columns[i],
                                'Variable 2': corr_matrix.columns[j],
                                'Correlación': corr_matrix.iloc[i, j]
                            })
                    
                    corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Correlación', key=abs, ascending=False)
                    st.dataframe(corr_pairs_df.head(10), use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis de dispersión
    if len(numeric_cols) >= 2:
        st.markdown("### 📍 Análisis de Dispersión")
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                x_var = st.selectbox("Variable X:", numeric_cols, key="scatter_x")
            with col2:
                y_var = st.selectbox("Variable Y:", [c for c in numeric_cols if c != x_var], key="scatter_y")
            
            if st.button("📊 Generar Gráfico de Dispersión", key="gen_scatter"):
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_scatter = generate_scatter_plot(df, x_var, y_var)
                    st.pyplot(fig_scatter)
                
                with col2:
                    fig_scatter_int = generate_interactive_scatter(df, x_var, y_var)
                    st.plotly_chart(fig_scatter_int, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)


def render_outlier_detection(df):
    """Renderiza la detección de outliers."""
    
    st.markdown('<p class="subtitle">Detección de Valores Atípicos (Outliers)</p>', unsafe_allow_html=True)
    
    numeric_cols = get_numeric_columns(df)
    
    if not numeric_cols:
        st.warning("⚠️ No hay variables numéricas para análisis de outliers.")
        return
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        selected_column = st.selectbox(
            "Seleccione la variable para análisis de outliers:",
            numeric_cols,
            key="outlier_column"
        )
        
        method = st.radio(
            "Método de detección:",
            ["IQR (Rango Intercuartílico)", "Z-Score"],
            key="outlier_method"
        )
        
        if method == "Z-Score":
            threshold = st.slider("Umbral de Z-score:", 1.0, 4.0, 3.0, 0.1, key="zscore_threshold")
        
        if st.button("🎯 Detectar Outliers", key="detect_outliers", use_container_width=True):
            with st.spinner('Detectando valores atípicos...'):
                data = df[selected_column].dropna()
                
                if method == "IQR (Rango Intercuartílico)":
                    outliers_info = detect_outliers_iqr(data)
                else:
                    outliers_info = detect_outliers_zscore(data, threshold)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("### 📊 Resultados")
                    for key, value in outliers_info.items():
                        if key != 'Valores Atípicos':
                            st.metric(key, value)
                
                with col2:
                    st.markdown("### 🎨 Visualización")
                    fig_outliers = generate_outliers_plot(data, outliers_info, selected_column)
                    st.pyplot(fig_outliers)
                
                if outliers_info['Valores Atípicos']:
                    st.markdown("### 📋 Valores Atípicos Detectados (Primeros 20)")
                    st.write(outliers_info['Valores Atípicos'])
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_normality_tests(df):
    """Renderiza las pruebas de normalidad."""
    
    st.markdown('<p class="subtitle">Pruebas de Normalidad</p>', unsafe_allow_html=True)
    
    numeric_cols = get_numeric_columns(df)
    
    if not numeric_cols:
        st.warning("⚠️ No hay variables numéricas para pruebas de normalidad.")
        return
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        selected_column = st.selectbox(
            "Seleccione la variable para pruebas de normalidad:",
            numeric_cols,
            key="normality_column"
        )
        
        if st.button("📐 Realizar Pruebas de Normalidad", key="test_normality", use_container_width=True):
            with st.spinner('Realizando pruebas estadísticas...'):
                data = df[selected_column].dropna()
                
                normality_results = test_normality(data)
                
                if 'error' in normality_results:
                    st.error(f"❌ {normality_results['error']}")
                else:
                    st.markdown("### 📊 Resultados de las Pruebas")
                    
                    for test_name, results in normality_results.items():
                        if 'error' not in results:
                            with st.expander(f"📌 {test_name}", expanded=True):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Estadístico", results['Estadístico'])
                                with col2:
                                    st.metric("p-valor", results['p-valor'])
                                with col3:
                                    is_normal = "✅ SÍ" if results['Es Normal (α=0.05)'] else "❌ NO"
                                    st.metric("¿Es Normal?", is_normal)
                                
                                interpretation = results['Interpretación']
                                if results['Es Normal (α=0.05)']:
                                    st.success(f"✅ {interpretation}")
                                else:
                                    st.warning(f"⚠️ {interpretation}")
                    
                    # Visualizaciones
                    st.markdown("### 📈 Visualizaciones")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Gráfico Q-Q")
                        fig_qq = generate_qq_plot(data, selected_column)
                        st.pyplot(fig_qq)
                    
                    with col2:
                        st.markdown("#### Comparación con Normal")
                        fig_dist = generate_distribution_comparison(data, selected_column)
                        st.pyplot(fig_dist)
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_export_section(df, selected_column, variable_type, frequency_table, measures, quartiles, figs):
    """Renderiza la sección de exportación."""
    
    st.markdown('<p class="subtitle">📥 Exportación de Resultados</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown("#### Seleccione los elementos a incluir:")
        col1, col2 = st.columns(2)
        
        with col1:
            include_freq_table = st.checkbox("Tabla de Frecuencia", value=True, key="export_freq")
            include_measures = st.checkbox("Medidas de Resumen", value=True, key="export_measures")
        
        with col2:
            include_quartiles = st.checkbox("Cuartiles", value=True, key="export_quartiles")
            include_graphs = st.checkbox("Gráficos", value=True, key="export_graphs")
        
        selected_items = []
        if include_freq_table:
            selected_items.append('tabla_frecuencia')
        if include_measures:
            selected_items.append('medidas_resumen')
        if include_quartiles:
            selected_items.append('cuartiles')
        if include_graphs:
            selected_items.append('graficos')
        
        st.markdown("#### Descargar Resultados:")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            excel_filename = f"Analisis_{selected_column}.xlsx"
            excel_data = export_to_excel(frequency_table, measures, quartiles, figs, selected_items, excel_filename)
            st.download_button(
                label="📊 Descargar Excel",
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col2:
            pdf_filename = f"Analisis_{selected_column}.pdf"
            pdf_data = export_to_pdf(df, selected_column, variable_type, frequency_table, measures, quartiles, figs, selected_items, pdf_filename)
            st.download_button(
                label="📄 Descargar PDF",
                data=pdf_data,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )
        
        with col3:
            html_report = generate_html_report(df, selected_column, variable_type, frequency_table, measures, quartiles, figs)
            html_filename = f"Informe_{selected_column}.html"
            st.download_button(
                label="🌐 Descargar HTML",
                data=html_report,
                file_name=html_filename,
                mime="text/html",
                use_container_width=True
            )
        
        with col4:
            # Obtener los valores originales de los datos
            data_values = df[selected_column].dropna().tolist()
            r_code = generate_r_code(df, selected_column, variable_type, frequency_table, measures, quartiles, data_values)
            r_filename = f"Codigo_R_{selected_column}.R"
            st.download_button(
                label="📈 Código R Studio",
                data=r_code,
                file_name=r_filename,
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
