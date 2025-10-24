"""
Módulo de exportación de resultados.
Contiene funciones para exportar a Excel, PDF, HTML y código R.
"""
import pandas as pd
import io
from datetime import datetime
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
import base64
from src.visualization import save_plot_for_pdf


def export_to_excel(frequency_table, measures, quartiles, graphs, selected_items, filename="Resultados.xlsx"):
    """
    Exporta los resultados a un archivo Excel.
    
    Args:
        frequency_table (list): Tabla de frecuencia
        measures (dict): Medidas estadísticas
        quartiles (dict): Cuartiles
        graphs: Gráficos (no se incluyen en Excel)
        selected_items (list): Items seleccionados para exportar
        filename (str): Nombre del archivo
        
    Returns:
        io.BytesIO: Buffer con el archivo Excel
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if 'tabla_frecuencia' in selected_items and frequency_table:
            pd.DataFrame(frequency_table).to_excel(writer, sheet_name='Tabla de Frecuencia', index=False)
        
        if 'medidas_resumen' in selected_items and measures:
            pd.DataFrame(list(measures.items()), columns=['Medida', 'Valor']).to_excel(
                writer, sheet_name='Medidas de Resumen', index=False
            )
        
        if 'cuartiles' in selected_items and quartiles and any(v is not None for v in quartiles.values()):
            pd.DataFrame(list(quartiles.items()), columns=['Cuartil', 'Valor']).to_excel(
                writer, sheet_name='Cuartiles', index=False
            )
    
    output.seek(0)
    return output


def export_to_pdf(df, selected_column, variable_type, frequency_table, measures, quartiles, figs, selected_items, filename="Resultados.pdf"):
    """
    Exporta los resultados a un archivo PDF.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        selected_column (str): Columna analizada
        variable_type (str): Tipo de variable
        frequency_table (list): Tabla de frecuencia
        measures (dict): Medidas estadísticas
        quartiles (dict): Cuartiles
        figs (list): Lista de figuras
        selected_items (list): Items seleccionados para exportar
        filename (str): Nombre del archivo
        
    Returns:
        io.BytesIO: Buffer con el archivo PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1
    subtitle_style = styles["Heading2"]
    subtitle_style.spaceAfter = 14
    normal_style = styles["Normal"]
    normal_style.spaceBefore = 6
    normal_style.spaceAfter = 6
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white]),
    ])
    
    elements = []
    
    # Título
    elements.append(Paragraph(f"Análisis Estadístico: {selected_column}", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"Tipo de variable: {variable_type}", normal_style))
    elements.append(Paragraph(f"Número de observaciones: {len(df[selected_column].dropna())}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Tabla de frecuencia
    if 'tabla_frecuencia' in selected_items and frequency_table:
        elements.append(Paragraph("Tabla de Frecuencia", subtitle_style))
        
        frequency_df = pd.DataFrame(frequency_table)
        all_columns = frequency_df.columns.tolist()
        max_cols_per_table = 6
        
        column_groups = [all_columns[i:i + max_cols_per_table] 
                         for i in range(0, len(all_columns), max_cols_per_table)]
        
        for group_idx, col_group in enumerate(column_groups):
            if group_idx > 0:
                elements.append(Paragraph(f"Tabla de Frecuencia (continuación {group_idx+1})", subtitle_style))
            
            if 'valor' in frequency_df.columns and 'valor' not in col_group:
                selected_cols = ['valor'] + col_group
            elif group_idx > 0:
                first_col = all_columns[0]
                selected_cols = [first_col] + col_group
                if first_col in col_group:
                    selected_cols.remove(first_col)
            else:
                selected_cols = col_group
            
            partial_df = frequency_df[selected_cols]
            
            if len(partial_df) > 40:
                partial_df = pd.concat([partial_df.head(20), partial_df.tail(20)])
                elements.append(Paragraph("(Se muestran las primeras y últimas 20 filas)", normal_style))
            
            data = [partial_df.columns.tolist()] + partial_df.values.tolist()
            col_widths = [min(80, 500/len(selected_cols)) for _ in selected_cols]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            
            elements.append(KeepTogether([table, Spacer(1, 12)]))
    
    # Medidas de resumen
    if 'medidas_resumen' in selected_items and measures:
        elements.append(Paragraph("Medidas de Resumen", subtitle_style))
        
        measures_data = [["Medida", "Valor"]]
        for measure, value in measures.items():
            if value is not None:
                if isinstance(value, (int, float)):
                    measures_data.append([measure, f"{value:.4f}"])
                else:
                    measures_data.append([measure, str(value)])
            else:
                measures_data.append([measure, "No disponible"])
        
        table = Table(measures_data, colWidths=[200, 200])
        table.setStyle(table_style)
        elements.append(KeepTogether([table, Spacer(1, 12)]))
    
    # Cuartiles
    if 'cuartiles' in selected_items and quartiles and any(v is not None for v in quartiles.values()):
        elements.append(Paragraph("Cuartiles", subtitle_style))
        
        quartiles_data = [["Cuartil", "Valor"]]
        for quartile, value in quartiles.items():
            if value is not None:
                if isinstance(value, (int, float)):
                    quartiles_data.append([quartile, f"{value:.4f}"])
                else:
                    quartiles_data.append([quartile, str(value)])
            else:
                quartiles_data.append([quartile, "No disponible"])
        
        table = Table(quartiles_data, colWidths=[200, 200])
        table.setStyle(table_style)
        elements.append(KeepTogether([table, Spacer(1, 12)]))
    
    # Gráficos
    if 'graficos' in selected_items and figs:
        elements.append(Paragraph("Visualizaciones", subtitle_style))
        
        for i, fig in enumerate(figs):
            if fig is not None:
                img_buf = save_plot_for_pdf(fig, f"graph_{i}")
                img = Image(img_buf, width=500, height=300)
                elements.append(img)
                elements.append(Spacer(1, 12))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_html_report(df, selected_column, variable_type, frequency_table, measures, quartiles, figs):
    """
    Genera un informe HTML completo.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        selected_column (str): Columna analizada
        variable_type (str): Tipo de variable
        frequency_table (list): Tabla de frecuencia
        measures (dict): Medidas estadísticas
        quartiles (dict): Cuartiles
        figs (list): Lista de figuras
        
    Returns:
        str: Código HTML del informe
    """
    graph_imgs = []
    for fig in figs:
        if fig is not None:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode()
            graph_imgs.append(f'<img src="data:image/png;base64,{img_str}" style="max-width:100%;">')
    
    freq_table_html = pd.DataFrame(frequency_table).to_html(index=False, classes='dataframe')
    
    measures_html = ""
    if measures:
        measures_df = pd.DataFrame(list(measures.items()), columns=['Medida', 'Valor'])
        measures_html = measures_df.to_html(index=False, classes='dataframe')
    
    quartiles_html = ""
    if quartiles and any(v is not None for v in quartiles.values()):
        quartiles_df = pd.DataFrame(list(quartiles.items()), columns=['Cuartil', 'Valor'])
        quartiles_html = quartiles_df.to_html(index=False, classes='dataframe')
    
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Informe Estadístico - {selected_column}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #2c3e50;
                margin-top: 30px;
            }}
            .dataframe {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            .dataframe th, .dataframe td {{
                text-align: left;
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}
            .dataframe th {{
                background-color: #3498db;
                color: white;
            }}
            .dataframe tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .graph-container {{
                margin: 30px 0;
                text-align: center;
            }}
            .footer {{
                margin-top: 50px;
                text-align: center;
                font-size: 12px;
                color: #7f8c8d;
                border-top: 1px solid #ddd;
                padding-top: 20px;
            }}
            @media print {{
                body {{ margin: 15mm; }}
                h2 {{ page-break-before: always; }}
                .no-break {{ page-break-inside: avoid; }}
            }}
        </style>
    </head>
    <body>
        <h1>Informe Estadístico: {selected_column}</h1>
        
        <p><strong>Fecha de generación:</strong> {now}</p>
        <p><strong>Tipo de variable:</strong> {variable_type}</p>
        <p><strong>Número de observaciones:</strong> {len(df[selected_column].dropna())}</p>
        
        <h2>Tabla de Frecuencia</h2>
        <div class="no-break">
            {freq_table_html}
        </div>
        
        <h2>Medidas de Resumen</h2>
        <div class="no-break">
            {measures_html}
        </div>
        
        <h2>Cuartiles</h2>
        <div class="no-break">
            {quartiles_html}
        </div>
        
        <h2>Visualizaciones</h2>
        <div class="graph-container">
            {"".join(graph_imgs)}
        </div>
        
        <div class="footer">
            Informe generado automáticamente por Análisis Estadístico v2.0<br>
            Desarrollado por JOSE CAMARENA MEZA
        </div>
    </body>
    </html>
    """
    return html


def generate_r_code(df, selected_column, variable_type, frequency_table, measures, quartiles, data_values):
    """
    Genera código R con los datos y el análisis estadístico.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        selected_column (str): Columna analizada
        variable_type (str): Tipo de variable
        frequency_table (list): Tabla de frecuencia
        measures (dict): Medidas estadísticas
        quartiles (dict): Cuartiles
        data_values (list): Valores originales de los datos
        
    Returns:
        str: Código R completo
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Preparar los datos
    if variable_type == "Cualitativa":
        # Para datos cualitativos, usar comillas
        data_str = ", ".join([f'"{str(v)}"' for v in data_values if pd.notna(v)])
        data_type = "character"
    else:
        # Para datos cuantitativos, sin comillas
        data_str = ", ".join([str(v) for v in data_values if pd.notna(v)])
        data_type = "numeric"
    
    # Construir el código R
    r_code = f"""# ============================================================
# Análisis Estadístico en R
# Variable: {selected_column}
# Tipo: {variable_type}
# Fecha: {now}
# Generado automáticamente por Análisis Estadístico v2.0
# ============================================================

# Cargar librerías necesarias
library(ggplot2)
library(dplyr)

# ============================================================
# DATOS ORIGINALES
# ============================================================

# Ingresar los datos
datos <- c({data_str})

# Convertir a data frame
df <- data.frame(
  {selected_column} = datos
)

# Ver primeras observaciones
head(df)

# Resumen básico
summary(df${selected_column})

# ============================================================
# TABLA DE FRECUENCIAS
# ============================================================

"""

    if variable_type == "Cualitativa" or variable_type == "Cuantitativa Discreta":
        r_code += f"""# Crear tabla de frecuencias
tabla_freq <- table(df${selected_column})

# Tabla de frecuencias absolutas
print("Frecuencias Absolutas:")
print(tabla_freq)

# Tabla de frecuencias relativas
tabla_rel <- prop.table(tabla_freq)
print("Frecuencias Relativas:")
print(round(tabla_rel, 4))

# Tabla de frecuencias porcentuales
tabla_porc <- prop.table(tabla_freq) * 100
print("Frecuencias Porcentuales:")
print(round(tabla_porc, 2))

# Frecuencias acumuladas
tabla_acum <- cumsum(tabla_freq)
print("Frecuencias Acumuladas:")
print(tabla_acum)

"""
    else:
        # Para variables continuas o discretas con intervalos
        r_code += f"""# Para variables continuas, crear intervalos
n <- length(df${selected_column})

# Calcular número de intervalos (Regla de Sturges)
k <- ceiling(1 + 3.322 * log10(n))

# Crear intervalos
intervalos <- cut(df${selected_column}, breaks = k, include.lowest = TRUE)

# Tabla de frecuencias
tabla_freq <- table(intervalos)
print("Frecuencias Absolutas por Intervalo:")
print(tabla_freq)

# Frecuencias relativas
tabla_rel <- prop.table(tabla_freq)
print("Frecuencias Relativas:")
print(round(tabla_rel, 4))

# Frecuencias porcentuales
tabla_porc <- prop.table(tabla_freq) * 100
print("Frecuencias Porcentuales:")
print(round(tabla_porc, 2))

"""

    # Agregar medidas estadísticas
    r_code += """
# ============================================================
# MEDIDAS ESTADÍSTICAS
# ============================================================

"""

    if variable_type != "Cualitativa":
        r_code += f"""# Medidas de tendencia central
media <- mean(df${selected_column}, na.rm = TRUE)
mediana <- median(df${selected_column}, na.rm = TRUE)

print(paste("Media:", round(media, 4)))
print(paste("Mediana:", round(mediana, 4)))

# Moda (valor más frecuente)
tabla_valores <- table(df${selected_column})
moda <- as.numeric(names(tabla_valores)[which.max(tabla_valores)])
print(paste("Moda:", moda))

# Medidas de dispersión
varianza <- var(df${selected_column}, na.rm = TRUE)
desv_std <- sd(df${selected_column}, na.rm = TRUE)
rango <- max(df${selected_column}, na.rm = TRUE) - min(df${selected_column}, na.rm = TRUE)

print(paste("Varianza:", round(varianza, 4)))
print(paste("Desviación Estándar:", round(desv_std, 4)))
print(paste("Rango:", round(rango, 4)))

# Coeficiente de variación
cv <- (desv_std / media) * 100
print(paste("Coeficiente de Variación:", round(cv, 2), "%"))

# Valores mínimo y máximo
print(paste("Mínimo:", min(df${selected_column}, na.rm = TRUE)))
print(paste("Máximo:", max(df${selected_column}, na.rm = TRUE)))

# ============================================================
# CUARTILES
# ============================================================

# Calcular cuartiles
Q1 <- quantile(df${selected_column}, 0.25, na.rm = TRUE)
Q2 <- quantile(df${selected_column}, 0.50, na.rm = TRUE)  # Mediana
Q3 <- quantile(df${selected_column}, 0.75, na.rm = TRUE)

print(paste("Q1 (Primer Cuartil):", round(Q1, 4)))
print(paste("Q2 (Segundo Cuartil/Mediana):", round(Q2, 4)))
print(paste("Q3 (Tercer Cuartil):", round(Q3, 4)))

# Rango intercuartílico
IQR_valor <- IQR(df${selected_column}, na.rm = TRUE)
print(paste("Rango Intercuartílico (IQR):", round(IQR_valor, 4)))

"""
    else:
        r_code += f"""# Para variables cualitativas
# Frecuencia del valor más común (moda)
tabla_valores <- table(df${selected_column})
moda <- names(tabla_valores)[which.max(tabla_valores)]
freq_moda <- max(tabla_valores)

print(paste("Moda:", moda))
print(paste("Frecuencia de la moda:", freq_moda))

# Proporción de la moda
prop_moda <- freq_moda / length(df${selected_column})
print(paste("Proporción de la moda:", round(prop_moda, 4)))

"""

    # Agregar código de visualización
    r_code += """
# ============================================================
# VISUALIZACIONES
# ============================================================

"""

    if variable_type == "Cualitativa":
        r_code += f"""# Gráfico de barras
ggplot(df, aes(x = {selected_column})) +
  geom_bar(fill = "steelblue", color = "black") +
  labs(title = "Distribución de {selected_column}",
       x = "{selected_column}",
       y = "Frecuencia") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Gráfico de pastel
tabla_freq <- table(df${selected_column})
pie(tabla_freq, 
    main = "Distribución de {selected_column}",
    col = rainbow(length(tabla_freq)),
    labels = paste(names(tabla_freq), 
                  "\n", round(prop.table(tabla_freq)*100, 1), "%"))

"""
    else:
        r_code += f"""# Histograma
ggplot(df, aes(x = {selected_column})) +
  geom_histogram(fill = "steelblue", color = "black", bins = 30) +
  labs(title = "Histograma de {selected_column}",
       x = "{selected_column}",
       y = "Frecuencia") +
  theme_minimal()

# Boxplot (diagrama de caja)
ggplot(df, aes(y = {selected_column})) +
  geom_boxplot(fill = "lightblue", color = "black") +
  labs(title = "Boxplot de {selected_column}",
       y = "{selected_column}") +
  theme_minimal()

# Gráfico de densidad
ggplot(df, aes(x = {selected_column})) +
  geom_density(fill = "steelblue", alpha = 0.5) +
  labs(title = "Densidad de {selected_column}",
       x = "{selected_column}",
       y = "Densidad") +
  theme_minimal()

# Q-Q Plot (para verificar normalidad)
qqnorm(df${selected_column}, main = "Q-Q Plot")
qqline(df${selected_column}, col = "red")

"""

    # Agregar comentarios sobre los resultados
    r_code += f"""
# ============================================================
# RESULTADOS OBTENIDOS (del análisis en Python)
# ============================================================

"""

    if measures:
        r_code += "# Medidas de resumen calculadas:\n"
        for key, value in measures.items():
            if value is not None and isinstance(value, (int, float)):
                r_code += f"# {key}: {value:.4f}\n"
            elif value is not None:
                r_code += f"# {key}: {value}\n"
        r_code += "\n"

    if quartiles and any(v is not None for v in quartiles.values()):
        r_code += "# Cuartiles calculados:\n"
        for key, value in quartiles.items():
            if value is not None and isinstance(value, (int, float)):
                r_code += f"# {key}: {value:.4f}\n"
            elif value is not None:
                r_code += f"# {key}: {value}\n"
        r_code += "\n"

    r_code += f"""# ============================================================
# NOTAS FINALES
# ============================================================

# Este código fue generado automáticamente basándose en el análisis
# realizado con Python. Puedes modificar y adaptar el código según
# tus necesidades específicas.
#
# Para ejecutar este código:
# 1. Asegúrate de tener instaladas las librerías necesarias
# 2. Ejecuta install.packages("ggplot2") si no tienes ggplot2
# 3. Ejecuta install.packages("dplyr") si no tienes dplyr
# 4. Copia y pega el código en RStudio
# 5. Ejecuta línea por línea o todo el script
#
# Desarrollado por: JOSE CAMARENA MEZA
# Fecha de generación: {now}
# ============================================================
"""

    return r_code

