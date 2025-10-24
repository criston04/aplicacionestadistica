# Análisis Estadístico Descriptivo v2.0 📊

> Aplicación web profesional para análisis estadístico completo con visualizaciones interactivas

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.43+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Características Principales

### ✨ Análisis Estadístico Completo
- **Tablas de Frecuencia**: Para variables cualitativas, cuantitativas discretas y continuas
- **Medidas de Tendencia Central**: Media, mediana, moda, media armónica y geométrica
- **Medidas de Dispersión**: Varianza, desviación estándar, coeficiente de variación
- **Cuartiles**: Q1, Q2 (mediana), Q3 con cálculo automático

### 🆕 Nuevas Funcionalidades v2.0

#### 🔗 Análisis de Correlación
- Matriz de correlación entre múltiples variables
- Mapas de calor interactivos
- Gráficos de dispersión con líneas de tendencia
- Identificación de correlaciones más fuertes

#### 🎯 Detección de Outliers
- Método IQR (Rango Intercuartílico)
- Método Z-Score con umbral configurable
- Visualización de valores atípicos
- Estadísticas detalladas de outliers

#### 📐 Pruebas de Normalidad
- Test de Shapiro-Wilk
- Test de Kolmogorov-Smirnov
- Test de D'Agostino-Pearson
- Gráficos Q-Q
- Comparación con distribución normal

### 📊 Visualizaciones Avanzadas
- Histogramas con KDE
- Gráficos de barras y pastel
- Boxplots y violin plots
- Gráficos interactivos con Plotly
- Mapas de calor de correlaciones
- Scatter plots con regresión

### 📥 Exportación Múltiple
- **Excel**: Tablas y estadísticas organizadas
- **PDF**: Informes profesionales con gráficos
- **HTML**: Reportes interactivos

## 🏗️ Estructura del Proyecto

```
aplicacionestadistica/
├── app.py                      # Aplicación principal (nueva versión modular)
├── criston.py                  # Versión original (legacy)
├── requirements.txt            # Dependencias
├── README.md                   # Documentación
├── src/                        # Código fuente modularizado
│   ├── __init__.py            # Inicialización del módulo
│   ├── config.py              # Configuraciones centralizadas
│   ├── utils.py               # Utilidades y helpers
│   ├── analysis.py            # Funciones de análisis estadístico
│   ├── visualization.py       # Funciones de visualización
│   └── export.py              # Funciones de exportación
├── data/                       # Datos de ejemplo
│   └── ejemplo_ventas.csv     # Dataset de ejemplo
└── tests/                      # Tests unitarios (próximamente)
    └── __init__.py
```

## 📋 Requisitos

- Python 3.7 o superior
- Dependencias especificadas en `requirements.txt`

## 🔧 Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/criston04/aplicacionestadistica.git
cd aplicacionestadistica
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

### Versión 2.0 (Recomendada - Modular)
```bash
streamlit run app.py
```

### Versión Original (Legacy)
```bash
streamlit run criston.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 📖 Uso

### 1️⃣ Cargar Datos
- Soporta archivos **CSV**, **XLSX** y **TXT**
- Configura el separador, formato decimal y codificación
- Tamaño máximo: 200 MB

### 2️⃣ Análisis Univariado
- Selecciona una columna para análisis
- La app detecta automáticamente el tipo de variable
- Maneja valores nulos según tus necesidades
- Obtén tablas de frecuencia y estadísticas completas

### 3️⃣ Análisis de Correlación
- Selecciona múltiples variables numéricas
- Genera matriz de correlación
- Visualiza relaciones con mapas de calor
- Crea gráficos de dispersión

### 4️⃣ Detección de Outliers
- Elige entre método IQR o Z-Score
- Visualiza outliers en boxplots
- Obtén listado de valores atípicos

### 5️⃣ Pruebas de Normalidad
- Realiza múltiples tests estadísticos
- Interpreta resultados automáticamente
- Visualiza con gráficos Q-Q

### 6️⃣ Exportar Resultados
- Selecciona componentes a incluir
- Descarga en formato Excel, PDF o HTML

## 🎨 Temas Visuales

La aplicación incluye 5 temas de visualización:
- **Default**: Tema claro estándar
- **Dark**: Tema oscuro
- **Blue**: Paleta azul
- **Green**: Paleta verde
- **Purple**: Paleta morada

## 📊 Tipos de Variables Soportados

### Cualitativas
- Nominal
- Ordinal

### Cuantitativas
- **Discretas**: Enteros con pocos valores únicos
- **Discretas con Intervalos**: Enteros con muchos valores únicos
- **Continuas**: Números decimales

## 🔬 Análisis Disponibles

### Estadísticas Descriptivas
- Media aritmética, armónica y geométrica
- Mediana y moda
- Varianza y desviación estándar
- Coeficiente de variación
- Cuartiles (Q1, Q2, Q3)
- Asimetría y curtosis

### Análisis Avanzados
- Correlación de Pearson
- Detección de outliers (IQR y Z-score)
- Tests de normalidad (Shapiro-Wilk, K-S, D'Agostino)
- Análisis de frecuencias

## 🛠️ Tecnologías Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework web
- **[Pandas](https://pandas.pydata.org/)**: Manipulación de datos
- **[NumPy](https://numpy.org/)**: Cálculos numéricos
- **[Matplotlib](https://matplotlib.org/)**: Visualización estática
- **[Seaborn](https://seaborn.pydata.org/)**: Visualización estadística
- **[Plotly](https://plotly.com/)**: Gráficos interactivos
- **[SciPy](https://scipy.org/)**: Análisis estadístico avanzado
- **[ReportLab](https://www.reportlab.com/)**: Generación de PDFs
- **[OpenPyXL](https://openpyxl.readthedocs.io/)**: Archivos Excel

## 📝 Mejoras en v2.0

✅ **Arquitectura Modular**: Código organizado en módulos separados  
✅ **Análisis de Correlación**: Nueva funcionalidad completa  
✅ **Detección de Outliers**: IQR y Z-Score  
✅ **Pruebas de Normalidad**: Tests estadísticos automáticos  
✅ **UI/UX Mejorada**: Tabs, cards, métricas visuales  
✅ **Caché Optimizado**: Mejor rendimiento con @st.cache_data  
✅ **Configuración Centralizada**: Archivo config.py  
✅ **Código Limpio**: Funciones documentadas y organizadas  

## 🔜 Próximas Mejoras

- [ ] Tests unitarios completos
- [ ] Análisis de regresión lineal
- [ ] Series temporales
- [ ] Machine Learning básico (clustering, PCA)
- [ ] Base de datos para historial
- [ ] API REST
- [ ] Soporte para más formatos (JSON, Parquet)
- [ ] Dashboard comparativo

## 👨‍💻 Autor

**JOSE CAMARENA MEZA**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un **Issue** en GitHub.

---

⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub!
