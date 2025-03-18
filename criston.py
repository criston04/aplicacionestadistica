import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.platypus.flowables import KeepTogether
# Asegúrate de que las bibliotecas estén instaladas
import plotly.express as px
import plotly.graph_objects as go

import io
import os
import streamlit as st
from math import log, exp
import base64
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Usar backend Agg para evitar problemas con threads

# Función para determinar el tipo de variable
def determine_variable_type(data):
    if any(not isinstance(x, (int, float)) for x in data):
        return "Cualitativa"
    if all(isinstance(x, int) for x in data):
        unique_values = len(set(data))
        return "Cuantitativa Discreta" if unique_values <= 10 else "Cuantitativa Discreta con Intervalos"
    return "Cuantitativa Continua"

# Función para calcular la tabla de frecuencia
def calculate_frequency_table(data, variable_type):
    frequency_table = []
    total_frecuencia_absoluta = 0
    total_frecuencia_relativa = 0
    total_frecuencia_porcentual = 0

    # Verificar y limpiar los datos
    if variable_type == "Cualitativa":
        # Convertir todos los valores a cadenas para evitar problemas de ordenación
        data = data.astype(str)
        unique_values = data.value_counts().sort_index()
        frecuencia_acumulada = 0
        for value, count in unique_values.items():
            frecuencia_acumulada += count
            frecuencia_relativa = count / len(data)
            frecuencia_relativa_acumulada = frecuencia_acumulada / len(data)
            frequency_table.append({
                'valor': value,
                'frecuenciaAbsoluta': count,
                'frecuenciaRelativa': round(frecuencia_relativa, 4),
                'frecuenciaPorcentual': round(frecuencia_relativa * 100, 2),
                'frecuenciaAcumulada': frecuencia_acumulada,
                'frecuenciaRelativaAcumulada': round(frecuencia_relativa_acumulada, 4),
                'frecuenciaPorcentualAcumulada': round(frecuencia_relativa_acumulada * 100, 2)
            })
            total_frecuencia_absoluta += count
            total_frecuencia_relativa += frecuencia_relativa
            total_frecuencia_porcentual += frecuencia_relativa * 100

    elif variable_type == "Cuantitativa Discreta":
        # Convertir todos los valores a números (por si hay valores no numéricos)
        data = pd.to_numeric(data, errors='coerce')
        # Eliminar valores NaN (si los hay)
        data = data.dropna()
        unique_values = data.value_counts().sort_index()
        frecuencia_acumulada = 0
        for value, count in unique_values.items():
            frecuencia_acumulada += count
            frecuencia_relativa = count / len(data)
            frecuencia_relativa_acumulada = frecuencia_acumulada / len(data)
            frequency_table.append({
                'valor': value,
                'frecuenciaAbsoluta': count,
                'frecuenciaRelativa': round(frecuencia_relativa, 4),
                'frecuenciaPorcentual': round(frecuencia_relativa * 100, 2),
                'frecuenciaAcumulada': frecuencia_acumulada,
                'frecuenciaRelativaAcumulada': round(frecuencia_relativa_acumulada, 4),
                'frecuenciaPorcentualAcumulada': round(frecuencia_relativa_acumulada * 100, 2)
            })
            total_frecuencia_absoluta += count
            total_frecuencia_relativa += frecuencia_relativa
            total_frecuencia_porcentual += frecuencia_relativa * 100

    elif variable_type in ["Cuantitativa Discreta con Intervalos", "Cuantitativa Continua"]:
        # Convertir todos los valores a números (por si hay valores no numéricos)
        data = pd.to_numeric(data, errors='coerce')
        # Eliminar valores NaN (si los hay)
        data = data.dropna()
        min_value = data.min()
        max_value = data.max()
        n = len(data)

        # Calcular el número de intervalos (k)
        k = 1 + 3.322 * np.log10(n)
        decimal_part = k - int(k)
        if decimal_part < 0.5:
            number_of_intervals = int(k)
        else:
            number_of_intervals = int(np.ceil(k))

        # Calcular el tamaño del intervalo
        interval_size = (max_value - min_value) / number_of_intervals

        # Crear los límites de los intervalos
        bins = [min_value + i * interval_size for i in range(number_of_intervals + 1)]
        bins[-1] += 0.001  # Ajuste para incluir el último valor

        # Crear los intervalos
        intervals = pd.cut(data, bins=bins, right=False)

        # Calcular frecuencias
        freq = intervals.value_counts().sort_index()

        # Generar la tabla de frecuencia
        frecuencia_acumulada = 0
        for interval, count in freq.items():
            frecuencia_acumulada += count
            frecuencia_relativa = count / n
            frecuencia_relativa_acumulada = frecuencia_acumulada / n

            # Calcular la marca de clase
            marca_clase = round((interval.left + interval.right) / 2, 3)

            frequency_table.append({
                'Intervalo': f"[{interval.left:.2f} - {interval.right:.2f})",
                'Marca de Clase': marca_clase,
                'Frecuencia Absoluta': count,
                'Frecuencia Acumulada': frecuencia_acumulada,
                'Frecuencia Relativa': round(frecuencia_relativa, 4),
                'Frecuencia Porcentual': f"{round(frecuencia_relativa * 100, 2)}%",
                'Frecuencia Relativa Acumulada': round(frecuencia_relativa_acumulada, 4),
                'Frecuencia Porcentual Acumulada': f"{round(frecuencia_relativa_acumulada * 100, 2)}%"
            })
            total_frecuencia_absoluta += count
            total_frecuencia_relativa += frecuencia_relativa
            total_frecuencia_porcentual += frecuencia_relativa * 100

    # Agregar fila de totales
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        frequency_table.append({
            'valor': 'Total',
            'frecuenciaAbsoluta': total_frecuencia_absoluta,
            'frecuenciaRelativa': round(total_frecuencia_relativa, 4),
            'frecuenciaPorcentual': round(total_frecuencia_porcentual, 2),
            'frecuenciaAcumulada': '',
            'frecuenciaRelativaAcumulada': '',
            'frecuenciaPorcentualAcumulada': ''
        })
    elif variable_type in ["Cuantitativa Discreta con Intervalos", "Cuantitativa Continua"]:
        frequency_table.append({
            'Intervalo': 'Total',
            'Marca de Clase': '',
            'Frecuencia Absoluta': total_frecuencia_absoluta,
            'Frecuencia Acumulada': '',
            'Frecuencia Relativa': round(total_frecuencia_relativa, 4),
            'Frecuencia Porcentual': f"{round(total_frecuencia_porcentual, 2)}%",
            'Frecuencia Relativa Acumulada': '',
            'Frecuencia Porcentual Acumulada': ''
        })

    return frequency_table

# Función para calcular medidas de tendencia central
def calculate_all_measures_grouped(frequency_table):
    """
    Calcula todas las medidas estadísticas para datos agrupados.
    
    Parámetros:
        frequency_table (list): Lista de diccionarios con la tabla de frecuencia.
        
    Retorna:
        dict: Diccionario con todas las medidas estadísticas.
    """
    # Verificar si la tabla de frecuencia está vacía
    if not frequency_table:
        return {}

    # Extraer marcas de clase, frecuencias e intervalos
    marcas_clase = []
    frecuencias = []
    intervalos = []
    
    for row in frequency_table:
        if 'Marca de Clase' in row and 'Frecuencia Absoluta' in row and 'Intervalo' in row:
            try:
                marca_clase = float(row['Marca de Clase'])
                frecuencia = int(row['Frecuencia Absoluta'])
                intervalo = row['Intervalo']
                marcas_clase.append(marca_clase)
                frecuencias.append(frecuencia)
                intervalos.append(intervalo)
            except (ValueError, KeyError):
                continue

    # Verificar si hay datos válidos
    if not marcas_clase or not frecuencias:
        return {}

    # Calcular la media
    total_frecuencia = sum(frecuencias)
    media = sum(marca * freq for marca, freq in zip(marcas_clase, frecuencias)) / total_frecuencia

    # Calcular la mediana
    frecuencia_acumulada = np.cumsum(frecuencias)
    n_2 = total_frecuencia / 2
    mediana = None

    for i, F in enumerate(frecuencia_acumulada):
        if F >= n_2:
            intervalo_mediano = intervalos[i]
            L = float(intervalo_mediano.split('[')[1].split(' - ')[0])  # Límite inferior
            F_anterior = frecuencia_acumulada[i - 1] if i > 0 else 0
            f_mediana = frecuencias[i]
            h = float(intervalo_mediano.split(' - ')[1].split(')')[0]) - L  # Amplitud
            mediana = L + ((n_2 - F_anterior) / f_mediana) * h
            break

    # Calcular la moda
    moda_index = np.argmax(frecuencias)
    moda = None

    if moda_index < len(intervalos):
        intervalo_modal = intervalos[moda_index]
        L = float(intervalo_modal.split('[')[1].split(' - ')[0])  # Límite inferior
        d1 = frecuencias[moda_index] - (frecuencias[moda_index - 1] if moda_index > 0 else 0)
        d2 = frecuencias[moda_index] - (frecuencias[moda_index + 1] if moda_index < len(frecuencias) - 1 else 0)
        h = float(intervalo_modal.split(' - ')[1].split(')')[0]) - L  # Amplitud
        if (d1 + d2) != 0:
            moda = L + (d1 / (d1 + d2)) * h
        else:
            moda = L  # Si d1 + d2 = 0, la moda es el límite inferior

    # Calcular la media armónica
    media_armonica = total_frecuencia / sum(freq / marca for marca, freq in zip(marcas_clase, frecuencias))

    # Calcular la media geométrica usando logaritmos
    suma_logs = sum(freq * log(marca) for marca, freq in zip(marcas_clase, frecuencias))
    media_geometrica = exp(suma_logs / total_frecuencia)

    # Calcular varianza y desviación estándar
    varianza = sum(freq * (marca - media) ** 2 for marca, freq in zip(marcas_clase, frecuencias)) / total_frecuencia
    desviacion_estandar = np.sqrt(varianza)

    # Calcular coeficiente de variación
    coeficiente_variacion = (desviacion_estandar / media) * 100 if media != 0 else 0

    # Retornar resultados
    return {
        'Media': round(media, 2),
        'Mediana': round(mediana, 2) if mediana is not None else None,
        'Moda': round(moda, 2) if moda is not None else None,
        'Media Armónica': round(media_armonica, 2),
        'Media Geométrica': round(media_geometrica, 2),
        'Varianza': round(varianza, 2),
        'Desviación Estándar': round(desviacion_estandar, 2),
        'Coeficiente de Variación (%)': round(coeficiente_variacion, 2)
    }

# Función para calcular cuartiles
def calculate_quartiles(data, frequency_table, variable_type):
    """
    Calcula los cuartiles (Q1, Q2, Q3) para datos agrupados o no agrupados.
    
    Parámetros:
        data (pd.Series): Los datos originales.
        frequency_table (list): La tabla de frecuencia.
        variable_type (str): El tipo de variable.
        
    Retorna:
        dict: Un diccionario con los cuartiles (Q1, Q2, Q3) o None si no se pueden calcular.
    """
    # Solo calcular cuartiles para variables cuantitativas
    if variable_type not in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos", "Cuantitativa Discreta"]:
        return {'Q1': None, 'Q2': None, 'Q3': None}

    # Verificar si hay suficientes datos
    if len(data) < 4:  # Necesitamos al menos 4 valores para calcular cuartiles
        return {'Q1': None, 'Q2': None, 'Q3': None}

    # Si la variable es discreta sin intervalos, calcular cuartiles directamente
    if variable_type == "Cuantitativa Discreta":
        try:
            # Ordenar los datos
            sorted_data = sorted(data.dropna())
            n = len(sorted_data)
            
            # Calcular posiciones para Q1, Q2 y Q3
            # Usando método de percentiles inclusivo
            q1_pos = (n + 1) * 0.25
            q2_pos = (n + 1) * 0.5
            q3_pos = (n + 1) * 0.75
            
            # Calcular valores de cuartiles por interpolación lineal
            def get_percentile(pos):
                if pos.is_integer():
                    return sorted_data[int(pos) - 1]
                else:
                    lower_pos = int(pos)
                    fraction = pos - lower_pos
                    lower_val = sorted_data[lower_pos - 1]
                    upper_val = sorted_data[lower_pos] if lower_pos < n else sorted_data[lower_pos - 1]
                    return lower_val + fraction * (upper_val - lower_val)
            
            q1 = get_percentile(q1_pos)
            q2 = get_percentile(q2_pos)
            q3 = get_percentile(q3_pos)
            
            return {'Q1': round(q1, 2), 'Q2': round(q2, 2), 'Q3': round(q3, 2)}
        except Exception as e:
            st.error(f"Error al calcular cuartiles para datos discretos: {e}")
            return {'Q1': None, 'Q2': None, 'Q3': None}

    # Para variables continuas o discretas con intervalos
    try:
        # Preparar datos necesarios de la tabla de frecuencia
        intervals = []
        frequencies = []
        
        for row in frequency_table:
            # Ignorar la fila de totales
            if row.get('Intervalo') != 'Total':
                try:
                    # Extraer límites del intervalo
                    interval_str = row.get('Intervalo', '')
                    if not isinstance(interval_str, str) or not interval_str:
                        continue
                        
                    # Extraer límites usando regex
                    import re
                    match = re.match(r'[\[\(](\d+\.?\d*)\s*-\s*(\d+\.?\d*)[\]\)]', interval_str)
                    if not match:
                        continue
                        
                    lower_limit = float(match.group(1))
                    upper_limit = float(match.group(2))
                    
                    intervals.append({
                        'lower': lower_limit,
                        'upper': upper_limit,
                        'width': upper_limit - lower_limit
                    })
                    
                    frequencies.append(row.get('Frecuencia Absoluta', 0))
                except (ValueError, TypeError, AttributeError) as e:
                    st.error(f"Error procesando intervalo '{row.get('Intervalo')}': {e}")
                    continue
        
        if not intervals or not frequencies:
            return {'Q1': None, 'Q2': None, 'Q3': None}
            
        # Calcular frecuencias acumuladas
        n = sum(frequencies)
        cum_freq = []
        cum_sum = 0
        for f in frequencies:
            cum_sum += f
            cum_freq.append(cum_sum)
            
        # Función para calcular cuartil k
        def calculate_quartile(k):
            position = k * n / 4
            
            # Encontrar el intervalo que contiene el cuartil
            interval_index = 0
            for i, cf in enumerate(cum_freq):
                if cf >= position:
                    interval_index = i
                    break
            
            # Extraer datos del intervalo
            interval = intervals[interval_index]
            lower_limit = interval['lower']
            interval_width = interval['width']
            interval_freq = frequencies[interval_index]
            
            # Frecuencia acumulada anterior
            prev_cum_freq = 0 if interval_index == 0 else cum_freq[interval_index - 1]
            
            # Aplicar fórmula de cuartil para datos agrupados
            quartile = lower_limit + ((position - prev_cum_freq) / interval_freq) * interval_width
            return round(quartile, 2)
        
        q1 = calculate_quartile(1)
        q2 = calculate_quartile(2)
        q3 = calculate_quartile(3)
        
        return {'Q1': q1, 'Q2': q2, 'Q3': q3}
    except Exception as e:
        st.error(f"Error al calcular cuartiles para datos agrupados: {e}")
        return {'Q1': None, 'Q2': None, 'Q3': None}

# ------------------- NUEVAS FUNCIONES DE VISUALIZACIÓN -------------------

# Función para generar histograma con Matplotlib
def generate_histogram(data, variable_type, column_name):
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data, kde=True, bins='auto', ax=ax, color='steelblue')
        plt.title(f'Histograma de Frecuencias - {column_name}', fontsize=15)
        plt.xlabel('Intervalos', fontsize=12)
        plt.ylabel('Frecuencia Absoluta', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        return fig

# Función para generar histograma con Plotly
def generate_interactive_histogram(data, variable_type, column_name):
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
        fig = px.histogram(
            data, 
            x=column_name,
            title=f'Histograma Interactivo - {column_name}',
            labels={'x': 'Valores', 'y': 'Frecuencia'},
            opacity=0.8,
            color_discrete_sequence=['steelblue'],
            marginal='box'  # Añade un boxplot en el margen
        )
        fig.update_layout(
            bargap=0.1,
            xaxis_title='Valores',
            yaxis_title='Frecuencia',
            template='plotly_white'
        )
        return fig

# Función para generar gráfico de pastel
def generate_pie_chart(data, variable_type, column_name):
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        fig, ax = plt.subplots(figsize=(10, 10))
        value_counts = data.value_counts()
        
        # Si hay muchas categorías, mostrar solo las 10 principales
        if len(value_counts) > 10:
            other_sum = value_counts.iloc[10:].sum()
            value_counts = value_counts.iloc[:10]
            if other_sum > 0:
                value_counts['Otros'] = other_sum
        
        wedges, texts, autotexts = ax.pie(
            value_counts, 
            autopct='%1.1f%%', 
            textprops={'color': "w", 'fontsize': 12},
            shadow=False, 
            startangle=90,
            explode=[0.05] * len(value_counts)  # Separar ligeramente todas las secciones
        )
        
        plt.title(f'Distribución de {column_name}', fontsize=16)
        ax.legend(
            wedges, 
            value_counts.index, 
            title="Categorías",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        plt.tight_layout()
        return fig

# Función para generar gráfico de barras
def generate_bar_chart(data, variable_type, column_name):
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        fig, ax = plt.subplots(figsize=(12, 8))
        value_counts = data.value_counts().sort_values(ascending=False)
        
        # Si hay muchas categorías, mostrar solo las 15 principales
        if len(value_counts) > 15:
            value_counts = value_counts.iloc[:15]
        
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette='viridis')
        plt.title(f'Gráfico de Barras - {column_name}', fontsize=15)
        plt.xlabel('Categorías', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        return fig

# Función para generar gráfico de barras horizontales
def generate_horizontal_bar_chart(data, variable_type, column_name):
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        fig, ax = plt.subplots(figsize=(12, max(6, min(20, len(data.value_counts())//2))))
        value_counts = data.value_counts().sort_values()
        
        # Si hay muchas categorías, mostrar solo las 20 principales
        if len(value_counts) > 20:
            value_counts = value_counts.tail(20)
        
        sns.barplot(y=value_counts.index, x=value_counts.values, ax=ax, palette='viridis', orient='h')
        plt.title(f'Gráfico de Barras Horizontales - {column_name}', fontsize=15)
        plt.ylabel('Categorías', fontsize=12)
        plt.xlabel('Frecuencia', fontsize=12)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        return fig

# Función para generar boxplot
def generate_boxplot(data, variable_type, column_name):
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta", "Cuantitativa Discreta con Intervalos"]:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=data, ax=ax, color='steelblue')
        plt.title(f'Diagrama de Caja - {column_name}', fontsize=15)
        plt.grid(axis='x', alpha=0.3)
        return fig

# Función para generar violin plot
def generate_violinplot(data, variable_type, column_name):
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta", "Cuantitativa Discreta con Intervalos"]:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(x=data, ax=ax, color='steelblue', inner='quartile')
        plt.title(f'Diagrama de Violín - {column_name}', fontsize=15)
        plt.grid(axis='x', alpha=0.3)
        return fig

# Función para guardar gráficos para el PDF
def save_plot_for_pdf(fig, filename):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf

# ------------------- FUNCIONES DE EXPORTACIÓN MEJORADAS -------------------

# Función para exportar a Excel con opciones personalizadas
def export_to_excel(frequency_table, measures, quartiles, graphs, selected_items, filename="Resultados.xlsx"):
    # Crear un archivo Excel en memoria
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Exportar la tabla de frecuencia si está seleccionada
        if 'tabla_frecuencia' in selected_items:
            pd.DataFrame(frequency_table).to_excel(writer, sheet_name='Tabla de Frecuencia', index=False)
        
        # Exportar las medidas de resumen si están seleccionadas
        if 'medidas_resumen' in selected_items and measures:
            pd.DataFrame(list(measures.items()), columns=['Medida', 'Valor']).to_excel(
                writer, sheet_name='Medidas de Resumen', index=False
            )
        
        # Exportar los cuartiles si están seleccionados
        if 'cuartiles' in selected_items and quartiles and any(v is not None for v in quartiles.values()):
            pd.DataFrame(list(quartiles.items()), columns=['Cuartil', 'Valor']).to_excel(
                writer, sheet_name='Cuartiles', index=False
            )
    
    # Preparar el archivo para descargar
    output.seek(0)
    return output

# Función para generar informe HTML
def generate_html_report(df, selected_column, variable_type, frequency_table, measures, quartiles, figs):
    """
    Genera un informe HTML completo con todos los análisis.
    """
    # Convertir gráficos a base64 para incluirlos en HTML
    graph_imgs = []
    for fig in figs:
        if fig is not None:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode()
            graph_imgs.append(f'<img src="data:image/png;base64,{img_str}" style="max-width:100%;">')
    
    # Crear tabla HTML para la tabla de frecuencia
    freq_table_html = pd.DataFrame(frequency_table).to_html(index=False, classes='dataframe')
    
    # Crear tabla HTML para las medidas
    measures_html = ""
    if measures:
        measures_df = pd.DataFrame(list(measures.items()), columns=['Medida', 'Valor'])
        measures_html = measures_df.to_html(index=False, classes='dataframe')
    
    # Crear tabla HTML para los cuartiles
    quartiles_html = ""
    if quartiles and any(v is not None for v in quartiles.values()):
        quartiles_df = pd.DataFrame(list(quartiles.items()), columns=['Cuartil', 'Valor'])
        quartiles_html = quartiles_df.to_html(index=False, classes='dataframe')
    
    # Fecha y hora actual
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Crear el HTML
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
            Informe generado automáticamente. Para más información contacte con el administrador.
        </div>
    </body>
    </html>
    """
    return html
#Exporta los resultados a un archivo PDF personalizado con soporte para tablas de frecuencia grandes.
def export_to_pdf(df, selected_column, variable_type, frequency_table, measures, quartiles, figs, selected_items, filename="Resultados.pdf"):
    """
    Exporta los resultados a un archivo PDF personalizado con soporte para tablas de frecuencia grandes.
    """
    # Configuración inicial del PDF
    buffer = io.BytesIO()
    # Usar landscape para tablas anchas
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1  # Centrado
    subtitle_style = styles["Heading2"]
    subtitle_style.spaceAfter = 14
    normal_style = styles["Normal"]
    normal_style.spaceBefore = 6
    normal_style.spaceAfter = 6
    
    # Estilo personalizado para tablas
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
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Reducir el tamaño de la fuente para tablas grandes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white]),
    ])
    
    # Lista para almacenar los elementos del PDF
    elements = []
    
    # Título e información general
    elements.append(Paragraph(f"Análisis Estadístico: {selected_column}", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"Tipo de variable: {variable_type}", normal_style))
    elements.append(Paragraph(f"Número de observaciones: {len(df[selected_column].dropna())}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Tabla de frecuencia si está seleccionada
    if 'tabla_frecuencia' in selected_items:
        elements.append(Paragraph("Tabla de Frecuencia", subtitle_style))
        
        # Convertir la tabla de frecuencia a formato para ReportLab
        frequency_df = pd.DataFrame(frequency_table)
        
        # En vez de reducir columnas, dividir la tabla en secciones si es necesario
        all_columns = frequency_df.columns.tolist()
        max_cols_per_table = 6  # Número máximo de columnas por tabla
        
        # Dividir las columnas en grupos manejables
        column_groups = [all_columns[i:i + max_cols_per_table] 
                         for i in range(0, len(all_columns), max_cols_per_table)]
        
        for group_idx, col_group in enumerate(column_groups):
            if group_idx > 0:
                elements.append(Paragraph(f"Tabla de Frecuencia (continuación {group_idx+1})", subtitle_style))
            
            # Incluir siempre la primera columna (valores o categorías) en cada grupo
            if 'valor' in frequency_df.columns and 'valor' not in col_group:
                selected_cols = ['valor'] + col_group
            elif group_idx > 0:
                # Si no hay columna 'valor', usar la primera columna original como identificador
                first_col = all_columns[0]
                selected_cols = [first_col] + col_group
                if first_col in col_group:
                    selected_cols.remove(first_col)  # Evitar duplicados
            else:
                selected_cols = col_group
            
            # Obtener el dataframe con las columnas seleccionadas
            partial_df = frequency_df[selected_cols]
            
            # Limitar el número de filas si es muy grande, pero mostrar más filas
            if len(partial_df) > 40:
                partial_df = pd.concat([partial_df.head(20), partial_df.tail(20)])
                elements.append(Paragraph("(Se muestran las primeras y últimas 20 filas)", normal_style))
            
            # Crear tabla para PDF
            data = [partial_df.columns.tolist()] + partial_df.values.tolist()
            
            # Ajustar el ancho de las columnas
            col_widths = [min(80, 500/len(selected_cols)) for _ in selected_cols]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            
            # Añadir la tabla al PDF con KeepTogether para evitar divisiones
            elements.append(KeepTogether([table, Spacer(1, 12)]))
    
    # Medidas de resumen si están seleccionadas
    if 'medidas_resumen' in selected_items and measures:
        elements.append(Paragraph("Medidas de Resumen", subtitle_style))
        
        # Convertir las medidas a formato de tabla
        measures_data = [["Medida", "Valor"]]
        for measure, value in measures.items():
            if value is not None:
                # Formatear números con 4 decimales para mejorar presentación
                if isinstance(value, (int, float)):
                    measures_data.append([measure, f"{value:.4f}"])
                else:
                    measures_data.append([measure, str(value)])
            else:
                measures_data.append([measure, "No disponible"])
        
        # Crear tabla para PDF
        table = Table(measures_data, colWidths=[200, 200])
        table.setStyle(table_style)
        elements.append(KeepTogether([table, Spacer(1, 12)]))
    
    # Cuartiles si están seleccionados
    if 'cuartiles' in selected_items and quartiles and any(v is not None for v in quartiles.values()):
        elements.append(Paragraph("Cuartiles", subtitle_style))
        
        # Convertir los cuartiles a formato de tabla
        quartiles_data = [["Cuartil", "Valor"]]
        for quartile, value in quartiles.items():
            if value is not None:
                if isinstance(value, (int, float)):
                    quartiles_data.append([quartile, f"{value:.4f}"])
                else:
                    quartiles_data.append([quartile, str(value)])
            else:
                quartiles_data.append([quartile, "No disponible"])
        
        # Crear tabla para PDF
        table = Table(quartiles_data, colWidths=[200, 200])
        table.setStyle(table_style)
        elements.append(KeepTogether([table, Spacer(1, 12)]))
    
    # Gráficos si están seleccionados
    if 'graficos' in selected_items and figs:
        elements.append(Paragraph("Visualizaciones", subtitle_style))
        
        for i, fig in enumerate(figs):
            if fig is not None:
                # Guardar la figura como imagen
                img_buf = save_plot_for_pdf(fig, f"graph_{i}")
                img = Image(img_buf, width=500, height=300)  # Ajustar tamaño para modo landscape
                elements.append(img)
                elements.append(Spacer(1, 12))
    
    # Construir el PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
# ------------------- INTERFAZ DE USUARIO MEJORADA -------------------

def main():
    st.set_page_config(
        page_title="Análisis Estadístico Descriptivo",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Estilo personalizado
    st.markdown("""<style>
        <style>
        .main {
            padding: 2rem;
        }
        .title {
            font-size: 3rem !important;
            color: #1E6091;
            text-align: center;
            margin-bottom: 2rem;
        }
        .subtitle {
            font-size: 1.5rem !important;
            font-weight: 600;
            color: #2C3E50;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        .card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #6c757d;
            font-size: 0.8rem;
        }
        .stButton button {
            background-color: #1E6091;
            color: white;
            font-weight: 600;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            width: 100%;
        }
        .stDownloadButton button {
            background-color: #28a745;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Título principal con estilo mejorado
    st.markdown('<p class="title">📊 Análisis Estadístico Descriptivo</p>', unsafe_allow_html=True)
    
    # Sidebar mejorada
    with st.sidebar:
        st.image("https://cdn.pixabay.com/photo/2018/09/18/11/19/business-3685935_960_720.png", width=100)
        st.markdown("### Configuración")
        
        # Subir archivo
        uploaded_file = st.file_uploader("Subir archivo CSV, XLSX o TXT", type=["csv", "xlsx", "txt"])
        
        # Configuración de separador y decimal
        st.markdown("#### Opciones de importación")
        with st.expander("Configuración de archivo"):
            separator = st.selectbox("Separador", [",", ";", "\t", "|", " "], index=0)
            decimal = st.selectbox("Separador decimal", [".", ","], index=0)
            encoding = st.selectbox("Codificación", ["utf-8", "latin-1", "ISO-8859-1"], index=0)
        
        # Tema de visualización
        st.markdown("#### Personalización")
        theme = st.selectbox("Tema de visualización", ["default", "dark", "blue", "green", "purple"], index=0)
        
        # Créditos
        st.markdown("---")
        st.markdown('<p class="footer">Desarrollado por JOSE CAMARENA MEZA<br>Versión 2.0</p>', unsafe_allow_html=True)
    
    # Aplicar tema seleccionado
    if theme == "dark":
        plt.style.use("dark_background")
        sns.set_theme(style="darkgrid")
    elif theme == "blue":
        sns.set_theme(style="whitegrid", palette="Blues_d")
    elif theme == "green":
        sns.set_theme(style="whitegrid", palette="Greens_d")
    elif theme == "purple":
        sns.set_theme(style="whitegrid", palette="Purples_d")
    else:
        sns.set_theme(style="whitegrid")
    
    # Contenido principal
    if uploaded_file is not None:
        try:
            # Cargar datos según el tipo de archivo
            if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
                df = pd.read_csv(uploaded_file, sep=separator, decimal=decimal, encoding=encoding)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            # Mostrar información del dataset con estilo mejorado
            st.markdown('<p class="subtitle">Vista previa de datos</p>', unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.dataframe(df.head(10))
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Filas", df.shape[0])
                with col2:
                    st.metric("Columnas", df.shape[1])
                with col3:
                    st.metric("Valores nulos", df.isna().sum().sum())
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Seleccionar columna para análisis
            st.markdown('<p class="subtitle">Selección de variables</p>', unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                selected_column = st.selectbox("Seleccione la columna a analizar:", df.columns)
                
                # Mostrar tipo de datos y estadísticas básicas
                column_dtype = df[selected_column].dtype
                st.info(f"Tipo de datos detectado: {column_dtype}")
                
                # Detectar y manejar valores nulos
                missing_values = df[selected_column].isna().sum()
                if missing_values > 0:
                    st.warning(f"La columna contiene {missing_values} valores nulos.")
                    handle_missing = st.radio(
                        "¿Cómo manejar los valores nulos?",
                        ["Eliminar", "Reemplazar por la media", "Reemplazar por la mediana", "Reemplazar por cero"]
                    )
                    
                    if handle_missing == "Eliminar":
                        df = df.dropna(subset=[selected_column])
                        st.success(f"Se eliminaron {missing_values} filas con valores nulos.")
                    elif handle_missing == "Reemplazar por la media":
                        if pd.api.types.is_numeric_dtype(df[selected_column]):
                            df[selected_column] = df[selected_column].fillna(df[selected_column].mean())
                            st.success(f"Se reemplazaron {missing_values} valores nulos por la media.")
                        else:
                            st.error("No se puede calcular la media para variables no numéricas.")
                    elif handle_missing == "Reemplazar por la mediana":
                        if pd.api.types.is_numeric_dtype(df[selected_column]):
                            df[selected_column] = df[selected_column].fillna(df[selected_column].median())
                            st.success(f"Se reemplazaron {missing_values} valores nulos por la mediana.")
                        else:
                            st.error("No se puede calcular la mediana para variables no numéricas.")
                    elif handle_missing == "Reemplazar por cero":
                        df[selected_column] = df[selected_column].fillna(0)
                        st.success(f"Se reemplazaron {missing_values} valores nulos por cero.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Determinar el tipo de variable
            data = df[selected_column].dropna()
            variable_type = determine_variable_type(data)
            
            # Aplicar análisis descriptivo
            st.markdown('<p class="subtitle">Análisis Descriptivo</p>', unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                # Mostrar tipo de variable detectado
                st.info(f"Tipo de variable detectado: {variable_type}")
                
                # Botón para iniciar análisis
                if st.button("Realizar Análisis", key="analyze_btn"):
                    with st.spinner('Analizando datos...'):
                        # Cálculo de tabla de frecuencia
                        frequency_table = calculate_frequency_table(data, variable_type)
                        
                        # Medidas de resumen y cuartiles
                        if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
                            measures = calculate_all_measures_grouped(frequency_table)
                        else:
                            # Para variables discretas y cualitativas, usar métodos estándar
                            if variable_type == "Cuantitativa Discreta":
                                measures = {
                                    'Media': round(data.mean(), 2),
                                    'Mediana': round(data.median(), 2),
                                    'Moda': round(data.mode()[0], 2) if not data.mode().empty else None,
                                    'Varianza': round(data.var(), 2),
                                    'Desviación Estándar': round(data.std(), 2),
                                    'Coeficiente de Variación (%)': round((data.std() / data.mean()) * 100, 2) if data.mean() != 0 else 0
                                }
                            else:  # Cualitativa
                                mode_value = data.mode()[0] if not data.mode().empty else None
                                measures = {
                                    'Moda': mode_value,
                                    'Frecuencia de la Moda': data.value_counts().iloc[0] if not data.value_counts().empty else 0,
                                    'Proporción de la Moda': round(data.value_counts().iloc[0] / len(data), 4) if not data.value_counts().empty else 0
                                }
                        
                        # Calcular cuartiles
                        quartiles = calculate_quartiles(data, frequency_table, variable_type)
                        
                        # Mostrar tabla de frecuencia
                        st.markdown("### Tabla de Frecuencia")
                        st.dataframe(pd.DataFrame(frequency_table))
                        
                        # Mostrar medidas de resumen en una tabla formateada
                        if measures:
                            st.markdown("### Medidas de Resumen")
                            measures_df = pd.DataFrame(list(measures.items()), columns=['Medida', 'Valor'])
                            st.table(measures_df)
                        
                        # Mostrar cuartiles si están disponibles
                        if quartiles and any(v is not None for v in quartiles.values()):
                            st.markdown("### Cuartiles")
                            quartiles_df = pd.DataFrame(list(quartiles.items()), columns=['Cuartil', 'Valor'])
                            st.table(quartiles_df)
                        
                        # Generar gráficos según el tipo de variable
                        st.markdown('<p class="subtitle">Visualizaciones</p>', unsafe_allow_html=True)
                        
                        # Lista para almacenar figuras generadas
                        figs = []
                        
                        # Distribuir visualizaciones en columnas
                        if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Histograma
                                fig_hist = generate_histogram(data, variable_type, selected_column)
                                if fig_hist:
                                    st.markdown("#### Histograma")
                                    st.pyplot(fig_hist)
                                    figs.append(fig_hist)
                            
                            with col2:
                                # Boxplot
                                fig_box = generate_boxplot(data, variable_type, selected_column)
                                if fig_box:
                                    st.markdown("#### Diagrama de Caja")
                                    st.pyplot(fig_box)
                                    figs.append(fig_box)
                            
                            # Histograma interactivo con Plotly
                            st.markdown("#### Histograma Interactivo")
                            fig_interactive = generate_interactive_histogram(data, variable_type, selected_column)
                            if fig_interactive:
                                st.plotly_chart(fig_interactive, use_container_width=True)
                            
                            # Violin plot
                            fig_violin = generate_violinplot(data, variable_type, selected_column)
                            if fig_violin:
                                st.markdown("#### Diagrama de Violín")
                                st.pyplot(fig_violin)
                                figs.append(fig_violin)
                                
                        elif variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Gráfico de barras
                                fig_bar = generate_bar_chart(data, variable_type, selected_column)
                                if fig_bar:
                                    st.markdown("#### Gráfico de Barras")
                                    st.pyplot(fig_bar)
                                    figs.append(fig_bar)
                            
                            with col2:
                                # Gráfico de pastel
                                fig_pie = generate_pie_chart(data, variable_type, selected_column)
                                if fig_pie:
                                    st.markdown("#### Gráfico de Pastel")
                                    st.pyplot(fig_pie)
                                    figs.append(fig_pie)
                            
                            # Gráfico de barras horizontales
                            fig_hbar = generate_horizontal_bar_chart(data, variable_type, selected_column)
                            if fig_hbar:
                                st.markdown("#### Gráfico de Barras Horizontales")
                                st.pyplot(fig_hbar)
                                figs.append(fig_hbar)
                        
                        # Opciones de exportación
                        st.markdown('<p class="subtitle">Exportación de Resultados</p>', unsafe_allow_html=True)
                        with st.container():
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            
                            # Selección de elementos a exportar
                            st.markdown("#### Seleccione los elementos a incluir:")
                            col1, col2 = st.columns(2)
                            with col1:
                                include_freq_table = st.checkbox("Tabla de Frecuencia", value=True)
                                include_measures = st.checkbox("Medidas de Resumen", value=True)
                            with col2:
                                include_quartiles = st.checkbox("Cuartiles", value=True)
                                include_graphs = st.checkbox("Gráficos", value=True)
                            
                            # Crear lista de elementos seleccionados
                            selected_items = []
                            if include_freq_table:
                                selected_items.append('tabla_frecuencia')
                            if include_measures:
                                selected_items.append('medidas_resumen')
                            if include_quartiles:
                                selected_items.append('cuartiles')
                            if include_graphs:
                                selected_items.append('graficos')
                            
                            # Botones de exportación
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                excel_filename = f"Analisis_{selected_column}.xlsx"
                                excel_data = export_to_excel(frequency_table, measures, quartiles, figs, selected_items, excel_filename)
                                st.download_button(
                                    label="📊 Descargar Excel",
                                    data=excel_data,
                                    file_name=excel_filename,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            
                            with col2:
                                pdf_filename = f"Analisis_{selected_column}.pdf"
                                pdf_data = export_to_pdf(df, selected_column, variable_type, frequency_table, measures, quartiles, figs, selected_items, pdf_filename)
                                st.download_button(
                                    label="📄 Descargar PDF",
                                    data=pdf_data,
                                    file_name=pdf_filename,
                                    mime="application/pdf"
                                )
                            
                            with col3:
                                # Generar informe HTML
                                html_report = generate_html_report(df, selected_column, variable_type, frequency_table, measures, quartiles, figs)
                                html_filename = f"Informe_{selected_column}.html"
                                st.download_button(
                                    label="🌐 Descargar HTML",
                                    data=html_report,
                                    file_name=html_filename,
                                    mime="text/html"
                                )
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
            st.exception(e)
    
    else:
        # Mostrar pantalla de bienvenida cuando no hay archivo cargado
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image("https://cdn.pixabay.com/photo/2018/09/18/11/19/business-3685935_960_720.png", width=150)
        
        with col2:
            st.markdown("""
            ## Bienvenido a la Aplicación de Análisis Estadístico
            
            Esta herramienta te permite realizar un análisis estadístico descriptivo completo de tus datos:
            
            - 📊 **Tablas de frecuencia** para variables cualitativas y cuantitativas
            - 📏 **Medidas de tendencia central y dispersión**
            - 📈 **Visualizaciones interactivas** adaptadas al tipo de variable
            - 📑 **Exportación personalizada** en múltiples formatos
            
            Para comenzar, carga un archivo CSV, XLSX o TXT desde el panel lateral.
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mostrar ejemplos de uso
        st.markdown('<p class="subtitle">¿Cómo utilizar esta aplicación?</p>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            tab1, tab2, tab3 = st.tabs(["Paso 1: Cargar datos", "Paso 2: Configurar análisis", "Paso 3: Exportar resultados"])
            
            with tab1:
                st.markdown("""
                1. Utiliza el selector de archivos en la barra lateral
                2. Soporta formatos CSV, XLSX y TXT
                3. Configura el separador y formato decimal si es necesario
                4. La aplicación mostrará una vista previa de los datos cargados
                """)
            
            with tab2:
                st.markdown("""
                1. Selecciona la columna que deseas analizar
                2. La aplicación detectará automáticamente el tipo de variable
                3. Decide cómo manejar los valores nulos si existen
                4. Haz clic en "Realizar Análisis" para ver los resultados
                """)
            
            with tab3:
                st.markdown("""
                1. Selecciona qué componentes deseas incluir en tu exportación
                2. Descarga los resultados en formato Excel, PDF o HTML
                3. Los archivos exportados incluirán todos los análisis y visualizaciones seleccionados
                4. Personaliza el tema visual desde la barra lateral para cambiar el aspecto de los gráficos
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

#python -m streamlit run criston.py  para ejecutar la aplicación en modo local