# Análisis Estadístico con Streamlit

Este proyecto es una aplicación web desarrollada con **Streamlit** que permite realizar un análisis estadístico descriptivo completo sobre un conjunto de datos. La aplicación es capaz de manejar tanto variables **cualitativas** como **cuantitativas**, generando tablas de frecuencia, medidas de tendencia central, gráficos interactivos y exportando los resultados en diferentes formatos (Excel, PDF, HTML).

## Características principales

1. **Carga de datos**: 
   - Soporta archivos en formato **CSV**, **XLSX** y **TXT**.
   - Permite configurar el separador, el formato decimal y la codificación del archivo.

2. **Análisis estadístico**:
   - **Tablas de frecuencia**: Genera tablas de frecuencia para variables cualitativas y cuantitativas (discretas y continuas).
   - **Medidas de tendencia central**: Calcula la media, mediana, moda, media armónica y media geométrica.
   - **Medidas de dispersión**: Calcula la varianza, desviación estándar y coeficiente de variación.
   - **Cuartiles**: Calcula los cuartiles (Q1, Q2, Q3) para variables cuantitativas.

3. **Visualizaciones**:
   - **Histograma**: Para variables cuantitativas continuas o discretas con intervalos.
   - **Gráfico de barras**: Para variables cualitativas o cuantitativas discretas.
   - **Gráfico de pastel**: Para variables cualitativas o cuantitativas discretas.
   - **Diagrama de caja**: Para variables cuantitativas.
   - **Diagrama de violín**: Para variables cuantitativas.
   - **Histograma interactivo**: Utilizando Plotly para una experiencia más dinámica.

4. **Exportación de resultados**:
   - **Excel**: Exporta la tabla de frecuencia, medidas de resumen y cuartiles en un archivo Excel.
   - **PDF**: Genera un informe en PDF con las tablas y gráficos seleccionados.
   - **HTML**: Crea un informe HTML interactivo con los resultados del análisis.
   - **📈 Código R Studio** ⭐ **NUEVO**: Genera código R completo con tus datos y análisis para usar en RStudio.

5. **Personalización**:
   - Permite seleccionar el tema de visualización (default, dark, blue, green, purple).
   - Manejo de valores nulos: Eliminar, reemplazar por la media, mediana o cero.

## Requisitos

Para ejecutar esta aplicación, necesitas tener instalado Python 3.7 o superior. Además, debes instalar las siguientes bibliotecas:

```bash
pip install pandas numpy matplotlib seaborn openpyxl reportlab plotly streamlit
```

## Ejecución local

Para ejecutar la aplicación en tu máquina local, sigue estos pasos:

1. Clona el repositorio o descarga el archivo `criston.py`.
2. Abre una terminal en la carpeta donde se encuentra el archivo.
3. Ejecuta el siguiente comando:

```bash
streamlit run criston.py
```

4. La aplicación se abrirá en tu navegador predeterminado en `http://localhost:8501`.

## Uso de la aplicación

1. **Carga de datos**:
   - En la barra lateral, selecciona "Subir archivo" y carga tu archivo CSV, XLSX o TXT.
   - Configura el separador, el formato decimal y la codificación si es necesario.

2. **Selección de columna**:
   - Selecciona la columna que deseas analizar.
   - La aplicación detectará automáticamente el tipo de variable (cualitativa, cuantitativa discreta o continua).

3. **Análisis descriptivo**:
   - Haz clic en "Realizar Análisis" para generar la tabla de frecuencia, medidas de resumen y cuartiles.
   - Explora las visualizaciones generadas según el tipo de variable.

4. **Exportación de resultados**:
   - Selecciona los elementos que deseas exportar (tabla de frecuencia, medidas de resumen, cuartiles, gráficos).
   - Descarga los resultados en formato Excel, PDF, HTML o **Código R** para RStudio.
   - **Nuevo**: El código R incluye tus datos originales y todo el análisis completo listo para ejecutar.

## 🌟 Nueva Funcionalidad: Exportación a R Studio

La aplicación ahora permite exportar el análisis completo a código de **R Studio**. Esta característica incluye:

- ✅ **Datos originales**: Todos tus datos listos para usar en R
- ✅ **Código completo**: Análisis estadístico reproducible
- ✅ **Visualizaciones**: Gráficos con ggplot2
- ✅ **Comentarios**: Código documentado y explicativo
- ✅ **Resultados**: Los valores calculados para comparación

### Cómo usar la exportación a R:

1. Realiza tu análisis en la aplicación web
2. Ve a la sección "4️⃣ Exportar"
3. Haz clic en **"📈 Código R Studio"**
4. Abre el archivo `.R` en RStudio
5. Instala las librerías necesarias: `ggplot2` y `dplyr`
6. ¡Ejecuta el código!

Para más detalles, consulta la **[Guía de Exportación a R](GUIA_EXPORTACION_R.md)**.

### Ejemplos incluidos:

- `EJEMPLO_Codigo_R_Precio.R`: Análisis de variable cuantitativa
- `EJEMPLO_Codigo_R_Categoria.R`: Análisis de variable cualitativa

## Ejemplos de uso

### Paso 1: Cargar datos
- Sube un archivo CSV con datos de ventas, por ejemplo.
- Configura el separador como "," y el formato decimal como ".".

### Paso 2: Configurar análisis
- Selecciona la columna "Ventas" para analizar.
- Decide cómo manejar los valores nulos (eliminar, reemplazar por la media, etc.).

### Paso 3: Exportar resultados
- Genera un informe en PDF con la tabla de frecuencia y un histograma.
- Descarga un archivo Excel con las medidas de resumen y cuartiles.

## Créditos

Este proyecto fue desarrollado por **JOSE CAMARENA MEZA** como parte de una herramienta de análisis estadístico descriptivo. Si tienes alguna pregunta o sugerencia, no dudes en contactarme.

---

¡Gracias por usar esta aplicación! Espero que te sea de gran utilidad para tus análisis estadísticos.
