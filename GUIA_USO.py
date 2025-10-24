"""
GUÍA DE USO RÁPIDO - Análisis Estadístico v2.0
==============================================

EJECUTAR LA APLICACIÓN:
----------------------
streamlit run app.py


COMANDOS ÚTILES:
---------------
# Versión antigua (legacy)
streamlit run criston.py

# Ejecutar con puerto específico
streamlit run app.py --server.port 8502

# Ejecutar sin abrir navegador
streamlit run app.py --server.headless true


ESTRUCTURA DE MÓDULOS:
---------------------
src/
├── config.py          → Configuraciones centralizadas
├── utils.py           → Funciones auxiliares (carga, validación, etc.)
├── analysis.py        → Análisis estadístico (frecuencias, correlación, outliers, normalidad)
├── visualization.py   → Gráficos (matplotlib, seaborn, plotly)
└── export.py          → Exportación (Excel, PDF, HTML)


NUEVAS FUNCIONALIDADES v2.0:
----------------------------

1. ANÁLISIS DE CORRELACIÓN:
   - Matriz de correlación entre variables numéricas
   - Mapas de calor (estáticos e interactivos)
   - Gráficos de dispersión con línea de tendencia
   - Identificación de correlaciones más fuertes

2. DETECCIÓN DE OUTLIERS:
   - Método IQR (Rango Intercuartílico)
   - Método Z-Score (umbral configurable)
   - Visualización de outliers en boxplots
   - Estadísticas detalladas

3. PRUEBAS DE NORMALIDAD:
   - Test de Shapiro-Wilk (mejor para n < 50)
   - Test de Kolmogorov-Smirnov
   - Test de D'Agostino-Pearson (n >= 8)
   - Gráficos Q-Q
   - Comparación con distribución normal

4. UI/UX MEJORADA:
   - Tabs para organizar análisis
   - Cards con sombras
   - Métricas visuales
   - Colores y estilos mejorados
   - Responsiva y moderna


ANÁLISIS DISPONIBLES:
--------------------

📊 ANÁLISIS UNIVARIADO:
   - Tablas de frecuencia
   - Medidas de tendencia central
   - Medidas de dispersión
   - Cuartiles
   - Visualizaciones adaptadas al tipo de variable

🔗 ANÁLISIS DE CORRELACIÓN:
   - Selección múltiple de variables
   - Matriz numérica
   - Heatmap estático e interactivo
   - Top correlaciones
   - Scatter plots

🎯 DETECCIÓN DE OUTLIERS:
   - Selección de método (IQR/Z-Score)
   - Límites calculados
   - Visualización dual (boxplot + scatter)
   - Listado de valores atípicos

📐 PRUEBAS DE NORMALIDAD:
   - Múltiples tests estadísticos
   - Interpretación automática
   - Q-Q plots
   - Comparación con curva normal


TIPOS DE VARIABLES SOPORTADOS:
------------------------------
✓ Cualitativas (nominal, ordinal)
✓ Cuantitativas Discretas (pocos valores únicos)
✓ Cuantitativas Discretas con Intervalos (muchos valores únicos)
✓ Cuantitativas Continuas (decimales)


FORMATOS DE EXPORTACIÓN:
------------------------
📊 Excel (.xlsx)  → Tablas organizadas en hojas
📄 PDF (.pdf)     → Informe profesional con gráficos
🌐 HTML (.html)   → Reporte interactivo web


TEMAS VISUALES:
--------------
- default  → Tema claro estándar
- dark     → Tema oscuro
- blue     → Paleta azul
- green    → Paleta verde
- purple   → Paleta morada


EJEMPLOS DE USO:
---------------

1. ANÁLISIS BÁSICO:
   a) Carga archivo CSV/XLSX/TXT
   b) Selecciona columna en tab "Análisis Univariado"
   c) Maneja valores nulos
   d) Click "Realizar Análisis Completo"
   e) Exporta resultados

2. CORRELACIÓN MÚLTIPLE:
   a) Ve al tab "Análisis de Correlación"
   b) Selecciona 2+ variables numéricas
   c) Click "Calcular Matriz de Correlación"
   d) Analiza heatmap y top correlaciones

3. DETECCIÓN DE OUTLIERS:
   a) Tab "Detección de Outliers"
   b) Selecciona variable numérica
   c) Elige método (IQR o Z-Score)
   d) Click "Detectar Outliers"
   e) Revisa visualización y listado

4. VERIFICAR NORMALIDAD:
   a) Tab "Pruebas de Normalidad"
   b) Selecciona variable numérica
   c) Click "Realizar Pruebas de Normalidad"
   d) Interpreta resultados (p-valor > 0.05 = normal)
   e) Revisa Q-Q plot


OPTIMIZACIONES:
--------------
✓ @st.cache_data en funciones de carga
✓ Código modular para mantenimiento
✓ Configuración centralizada
✓ Validaciones robustas
✓ Manejo de errores mejorado


TIPS Y MEJORES PRÁCTICAS:
-------------------------
• Usa archivos CSV con encoding UTF-8 para evitar problemas
• Para archivos grandes, considera filtrar columnas antes
• Los gráficos interactivos son mejores para exploración
• Los PDFs son mejores para presentaciones formales
• Prueba con data/ejemplo_ventas.csv incluido


SOLUCIÓN DE PROBLEMAS:
---------------------

Error: Module not found
→ pip install -r requirements.txt

Error: Encoding
→ Cambia encoding en sidebar a 'latin-1' o 'ISO-8859-1'

Error: Memoria
→ Reduce tamaño del archivo o filtra datos

Gráficos no se muestran
→ Verifica que matplotlib backend sea 'Agg'


CONTACTO Y SOPORTE:
------------------
Desarrollado por: JOSE CAMARENA MEZA
Versión: 2.0
Año: 2025

Para reportar bugs o sugerencias:
→ Abre un Issue en GitHub
→ Contribuye con Pull Requests
"""

# Este archivo es solo documentación
# Para ejecutar la app usa: streamlit run app.py
