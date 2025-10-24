"""
Módulo de análisis estadístico.
Contiene funciones para calcular tablas de frecuencia, medidas estadísticas y cuartiles.
"""
import pandas as pd
import numpy as np
import streamlit as st
from math import log, exp
from scipy import stats
import re


def calculate_frequency_table(data, variable_type):
    """
    Calcula la tabla de frecuencia para diferentes tipos de variables.
    
    Args:
        data (pd.Series): Datos a analizar
        variable_type (str): Tipo de variable
        
    Returns:
        list: Lista de diccionarios con la tabla de frecuencia
    """
    frequency_table = []
    total_frecuencia_absoluta = 0
    total_frecuencia_relativa = 0
    total_frecuencia_porcentual = 0

    if variable_type == "Cualitativa":
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
        data = pd.to_numeric(data, errors='coerce')
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
        data = pd.to_numeric(data, errors='coerce')
        data = data.dropna()
        min_value = data.min()
        max_value = data.max()
        n = len(data)

        # Calcular el número de intervalos usando múltiples reglas y elegir la mejor
        # Regla de Sturges (clásica)
        k_sturges = int(np.ceil(1 + 3.322 * np.log10(n)))
        
        # Regla de Rice (alternativa)
        k_rice = int(np.ceil(2 * np.power(n, 1/3)))
        
        # Regla de Scott (basada en desviación estándar)
        h_scott = 3.5 * data.std() / np.power(n, 1/3)
        k_scott = int(np.ceil((max_value - min_value) / h_scott)) if h_scott > 0 else k_sturges
        
        # Regla de Freedman-Diaconis (más robusta)
        iqr = data.quantile(0.75) - data.quantile(0.25)
        h_fd = 2 * iqr / np.power(n, 1/3) if iqr > 0 else h_scott
        k_fd = int(np.ceil((max_value - min_value) / h_fd)) if h_fd > 0 else k_sturges
        
        # Elegir el número óptimo de intervalos (promedio ponderado)
        # Preferir métodos robustos pero limitar valores extremos
        k_options = [k_sturges, k_rice, k_scott, k_fd]
        k_options = [k for k in k_options if 5 <= k <= 30]  # Limitar entre 5 y 30 intervalos
        
        if k_options:
            number_of_intervals = int(np.median(k_options))  # Usar mediana para robustez
        else:
            number_of_intervals = max(5, min(20, k_sturges))  # Valor por defecto seguro
        
        # Ajustar si hay muy pocos datos
        if n < 30:
            number_of_intervals = min(number_of_intervals, int(np.sqrt(n)))

        # Calcular el tamaño del intervalo con precisión
        interval_size = (max_value - min_value) / number_of_intervals
        
        # Redondear el tamaño del intervalo a un valor "limpio" si es apropiado
        # Esto mejora la legibilidad sin perder precisión
        magnitude = 10 ** np.floor(np.log10(interval_size))
        interval_size_rounded = np.ceil(interval_size / magnitude) * magnitude
        
        # Recalcular número de intervalos con el tamaño redondeado
        if interval_size_rounded > 0:
            number_of_intervals = int(np.ceil((max_value - min_value) / interval_size_rounded))
            interval_size = interval_size_rounded

        # Crear los límites de los intervalos con precisión
        bins = [min_value + i * interval_size for i in range(number_of_intervals + 1)]
        bins[-1] = max_value + 0.0001  # Ajuste mínimo para incluir el último valor

        # Crear los intervalos usando pd.cut con precisión
        intervals = pd.cut(data, bins=bins, right=False, include_lowest=True)

        # Calcular frecuencias
        freq = intervals.value_counts().sort_index()

        # Generar la tabla de frecuencia
        frecuencia_acumulada = 0
        for interval, count in freq.items():
            frecuencia_acumulada += count
            frecuencia_relativa = count / n
            frecuencia_relativa_acumulada = frecuencia_acumulada / n

            # Calcular la marca de clase (punto medio del intervalo)
            marca_clase = (interval.left + interval.right) / 2

            frequency_table.append({
                'Intervalo': f"[{interval.left:.4f} - {interval.right:.4f})",
                'Marca de Clase': round(marca_clase, 4),
                'Frecuencia Absoluta': count,
                'Frecuencia Acumulada': frecuencia_acumulada,
                'Frecuencia Relativa': round(frecuencia_relativa, 6),
                'Frecuencia Porcentual': f"{round(frecuencia_relativa * 100, 2)}%",
                'Frecuencia Relativa Acumulada': round(frecuencia_relativa_acumulada, 6),
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
            'frecuenciaAcumulada': None,
            'frecuenciaRelativaAcumulada': None,
            'frecuenciaPorcentualAcumulada': None
        })
    elif variable_type in ["Cuantitativa Discreta con Intervalos", "Cuantitativa Continua"]:
        frequency_table.append({
            'Intervalo': 'Total',
            'Marca de Clase': None,
            'Frecuencia Absoluta': total_frecuencia_absoluta,
            'Frecuencia Acumulada': None,
            'Frecuencia Relativa': round(total_frecuencia_relativa, 4),
            'Frecuencia Porcentual': f"{round(total_frecuencia_porcentual, 2)}%",
            'Frecuencia Relativa Acumulada': None,
            'Frecuencia Porcentual Acumulada': None
        })

    return frequency_table


def calculate_all_measures_grouped(frequency_table):
    """
    Calcula todas las medidas estadísticas para datos agrupados con métodos precisos.
    
    Utiliza fórmulas interpoladas para:
    - Media ponderada por marca de clase
    - Mediana por interpolación lineal en la clase mediana
    - Moda por interpolación en la clase modal
    - Varianza con corrección para datos agrupados
    
    Args:
        frequency_table (list): Lista de diccionarios con la tabla de frecuencia
        
    Returns:
        dict: Diccionario con todas las medidas estadísticas precisas
    """
    if not frequency_table:
        return {}

    marcas_clase = []
    frecuencias = []
    intervalos = []
    limites_inf = []
    limites_sup = []
    
    for row in frequency_table:
        if 'Marca de Clase' in row and 'Frecuencia Absoluta' in row and 'Intervalo' in row:
            # Saltar filas con valores None (como la fila de totales)
            if row['Marca de Clase'] is None or row['Intervalo'] is None:
                continue
            
            try:
                marca_clase = float(row['Marca de Clase'])
                frecuencia = int(row['Frecuencia Absoluta'])
                intervalo = row['Intervalo']
                
                # Extraer límites del intervalo con precisión
                import re
                match = re.match(r'[\[\(](\d+\.?\d*)\s*-\s*(\d+\.?\d*)[\]\)]', str(intervalo))
                if match:
                    lim_inf = float(match.group(1))
                    lim_sup = float(match.group(2))
                    
                    marcas_clase.append(marca_clase)
                    frecuencias.append(frecuencia)
                    intervalos.append(intervalo)
                    limites_inf.append(lim_inf)
                    limites_sup.append(lim_sup)
            except (ValueError, KeyError, TypeError):
                continue

    if not marcas_clase or not frecuencias:
        return {}

    # Tamaño de muestra
    n = sum(frecuencias)
    
    # Calcular la MEDIA (promedio ponderado)
    media = sum(marca * freq for marca, freq in zip(marcas_clase, frecuencias)) / n

    # Calcular la MEDIANA con interpolación lineal mejorada
    frecuencia_acumulada = np.cumsum(frecuencias)
    n_2 = n / 2.0  # Posición de la mediana
    mediana = None

    for i, F_i in enumerate(frecuencia_acumulada):
        if F_i >= n_2:
            L_i = limites_inf[i]  # Límite inferior de la clase mediana
            F_ant = frecuencia_acumulada[i - 1] if i > 0 else 0  # Frecuencia acumulada anterior
            f_i = frecuencias[i]  # Frecuencia de la clase mediana
            c_i = limites_sup[i] - limites_inf[i]  # Amplitud del intervalo
            
            # Fórmula de interpolación lineal para la mediana
            mediana = L_i + ((n_2 - F_ant) / f_i) * c_i
            break

    # Calcular la MODA con interpolación (método de King)
    max_freq = max(frecuencias)
    moda_indices = [i for i, f in enumerate(frecuencias) if f == max_freq]
    
    if moda_indices:
        moda_index = moda_indices[0]  # Si hay varias, tomar la primera
        L_i = limites_inf[moda_index]  # Límite inferior de la clase modal
        f_i = frecuencias[moda_index]  # Frecuencia de la clase modal
        f_ant = frecuencias[moda_index - 1] if moda_index > 0 else 0  # Frecuencia anterior
        f_post = frecuencias[moda_index + 1] if moda_index < len(frecuencias) - 1 else 0  # Frecuencia posterior
        c_i = limites_sup[moda_index] - limites_inf[moda_index]  # Amplitud
        
        # Fórmula de King para la moda
        d1 = f_i - f_ant  # Diferencia con la clase anterior
        d2 = f_i - f_post  # Diferencia con la clase posterior
        
        if (d1 + d2) != 0:
            moda = L_i + (d1 / (d1 + d2)) * c_i
        else:
            moda = marcas_clase[moda_index]  # Si no se puede interpolar, usar marca de clase
    else:
        moda = None

    # Calcular MEDIA ARMÓNICA (solo si todas las marcas son positivas)
    if all(m > 0 for m in marcas_clase):
        media_armonica = n / sum(freq / marca for marca, freq in zip(marcas_clase, frecuencias))
    else:
        media_armonica = None

    # Calcular MEDIA GEOMÉTRICA (solo si todas las marcas son positivas)
    if all(m > 0 for m in marcas_clase):
        try:
            suma_logs = sum(freq * np.log(marca) for marca, freq in zip(marcas_clase, frecuencias))
            media_geometrica = np.exp(suma_logs / n)
        except:
            media_geometrica = None
    else:
        media_geometrica = None

    # Calcular VARIANZA para datos agrupados
    # Usando la fórmula: Var = Σ(f_i * (x_i - μ)²) / n
    varianza = sum(freq * (marca - media) ** 2 for marca, freq in zip(marcas_clase, frecuencias)) / n
    
    # Varianza muestral (con corrección n-1) - más apropiada para muestras
    varianza_muestral = sum(freq * (marca - media) ** 2 for marca, freq in zip(marcas_clase, frecuencias)) / (n - 1) if n > 1 else varianza
    
    # DESVIACIÓN ESTÁNDAR
    desviacion_estandar = np.sqrt(varianza)
    desviacion_estandar_muestral = np.sqrt(varianza_muestral)

    # COEFICIENTE DE VARIACIÓN
    coeficiente_variacion = (desviacion_estandar / media) * 100 if media != 0 else 0

    # ASIMETRÍA (usando momento de tercer orden)
    momento_3 = sum(freq * (marca - media) ** 3 for marca, freq in zip(marcas_clase, frecuencias)) / n
    asimetria = momento_3 / (desviacion_estandar ** 3) if desviacion_estandar > 0 else 0
    
    # CURTOSIS (usando momento de cuarto orden - exceso)
    momento_4 = sum(freq * (marca - media) ** 4 for marca, freq in zip(marcas_clase, frecuencias)) / n
    curtosis = (momento_4 / (desviacion_estandar ** 4)) - 3 if desviacion_estandar > 0 else 0

    # ERROR ESTÁNDAR de la media
    error_estandar = desviacion_estandar_muestral / np.sqrt(n)

    return {
        'N (Tamaño)': n,
        'Media': round(media, 4),
        'Mediana': round(mediana, 4) if mediana is not None else None,
        'Moda': round(moda, 4) if moda is not None else None,
        'Media Armónica': round(media_armonica, 4) if media_armonica is not None else 'N/A',
        'Media Geométrica': round(media_geometrica, 4) if media_geometrica is not None else 'N/A',
        'Varianza Poblacional': round(varianza, 4),
        'Varianza Muestral': round(varianza_muestral, 4),
        'Desviación Estándar Poblacional': round(desviacion_estandar, 4),
        'Desviación Estándar Muestral': round(desviacion_estandar_muestral, 4),
        'Coeficiente de Variación (%)': round(coeficiente_variacion, 2),
        'Error Estándar': round(error_estandar, 4),
        'Asimetría': round(asimetria, 4),
        'Curtosis (Exceso)': round(curtosis, 4),
        'Mínimo Observado': round(min(limites_inf), 4),
        'Máximo Observado': round(max(limites_sup), 4),
        'Rango': round(max(limites_sup) - min(limites_inf), 4)
    }


def calculate_quartiles(data, frequency_table, variable_type):
    """
    Calcula los cuartiles (Q1, Q2, Q3) para datos agrupados o no agrupados.
    
    Args:
        data (pd.Series): Los datos originales
        frequency_table (list): La tabla de frecuencia
        variable_type (str): El tipo de variable
        
    Returns:
        dict: Un diccionario con los cuartiles (Q1, Q2, Q3)
    """
    if variable_type not in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos", "Cuantitativa Discreta"]:
        return {'Q1': None, 'Q2': None, 'Q3': None}

    if len(data) < 4:
        return {'Q1': None, 'Q2': None, 'Q3': None}

    if variable_type == "Cuantitativa Discreta":
        try:
            sorted_data = sorted(data.dropna())
            n = len(sorted_data)
            
            q1_pos = (n + 1) * 0.25
            q2_pos = (n + 1) * 0.5
            q3_pos = (n + 1) * 0.75
            
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

    try:
        intervals = []
        frequencies = []
        
        for row in frequency_table:
            if row.get('Intervalo') != 'Total':
                try:
                    interval_str = row.get('Intervalo', '')
                    if not isinstance(interval_str, str) or not interval_str:
                        continue
                        
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
            
        n = sum(frequencies)
        cum_freq = []
        cum_sum = 0
        for f in frequencies:
            cum_sum += f
            cum_freq.append(cum_sum)
            
        def calculate_quartile(k):
            position = k * n / 4
            
            interval_index = 0
            for i, cf in enumerate(cum_freq):
                if cf >= position:
                    interval_index = i
                    break
            
            interval = intervals[interval_index]
            lower_limit = interval['lower']
            interval_width = interval['width']
            interval_freq = frequencies[interval_index]
            
            prev_cum_freq = 0 if interval_index == 0 else cum_freq[interval_index - 1]
            
            quartile = lower_limit + ((position - prev_cum_freq) / interval_freq) * interval_width
            return round(quartile, 2)
        
        q1 = calculate_quartile(1)
        q2 = calculate_quartile(2)
        q3 = calculate_quartile(3)
        
        return {'Q1': q1, 'Q2': q2, 'Q3': q3}
    except Exception as e:
        st.error(f"Error al calcular cuartiles para datos agrupados: {e}")
        return {'Q1': None, 'Q2': None, 'Q3': None}


# ============= NUEVAS FUNCIONALIDADES =============

def calculate_correlation_matrix(df, columns=None):
    """
    Calcula la matriz de correlación para variables numéricas.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columns (list): Lista de columnas a incluir (None = todas las numéricas)
        
    Returns:
        pd.DataFrame: Matriz de correlación
    """
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
    else:
        numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if len(numeric_cols) < 2:
        return None
    
    return df[numeric_cols].corr()


def detect_outliers_iqr(data):
    """
    Detecta valores atípicos usando el método IQR (Rango Intercuartílico).
    
    Args:
        data (pd.Series): Serie de datos numéricos
        
    Returns:
        dict: Información sobre outliers
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    
    return {
        'Q1': round(Q1, 2),
        'Q3': round(Q3, 2),
        'IQR': round(IQR, 2),
        'Límite Inferior': round(lower_bound, 2),
        'Límite Superior': round(upper_bound, 2),
        'Número de Outliers': len(outliers),
        'Porcentaje': round((len(outliers) / len(data)) * 100, 2),
        'Valores Atípicos': outliers.tolist()[:20]  # Primeros 20
    }


def detect_outliers_zscore(data, threshold=3):
    """
    Detecta valores atípicos usando el método Z-score.
    
    Args:
        data (pd.Series): Serie de datos numéricos
        threshold (float): Umbral de Z-score (por defecto 3)
        
    Returns:
        dict: Información sobre outliers
    """
    mean = data.mean()
    std = data.std()
    z_scores = np.abs((data - mean) / std)
    
    outliers = data[z_scores > threshold]
    
    return {
        'Media': round(mean, 2),
        'Desviación Estándar': round(std, 2),
        'Umbral Z-score': threshold,
        'Número de Outliers': len(outliers),
        'Porcentaje': round((len(outliers) / len(data)) * 100, 2),
        'Valores Atípicos': outliers.tolist()[:20]  # Primeros 20
    }


def test_normality(data):
    """
    Realiza pruebas de normalidad sobre los datos.
    
    Args:
        data (pd.Series): Serie de datos numéricos
        
    Returns:
        dict: Resultados de las pruebas de normalidad
    """
    data_clean = data.dropna()
    
    if len(data_clean) < 3:
        return {
            'error': 'Datos insuficientes para realizar pruebas de normalidad (mínimo 3 valores)'
        }
    
    results = {}
    
    # Prueba de Shapiro-Wilk (mejor para n < 50)
    if len(data_clean) <= 5000:
        try:
            shapiro_stat, shapiro_p = stats.shapiro(data_clean)
            results['Shapiro-Wilk'] = {
                'Estadístico': round(shapiro_stat, 4),
                'p-valor': round(shapiro_p, 4),
                'Es Normal (α=0.05)': shapiro_p > 0.05,
                'Interpretación': 'Los datos siguen una distribución normal' if shapiro_p > 0.05 
                                 else 'Los datos NO siguen una distribución normal'
            }
        except Exception as e:
            results['Shapiro-Wilk'] = {'error': str(e)}
    
    # Prueba de Kolmogorov-Smirnov
    try:
        ks_stat, ks_p = stats.kstest(data_clean, 'norm', args=(data_clean.mean(), data_clean.std()))
        results['Kolmogorov-Smirnov'] = {
            'Estadístico': round(ks_stat, 4),
            'p-valor': round(ks_p, 4),
            'Es Normal (α=0.05)': ks_p > 0.05,
            'Interpretación': 'Los datos siguen una distribución normal' if ks_p > 0.05 
                             else 'Los datos NO siguen una distribución normal'
        }
    except Exception as e:
        results['Kolmogorov-Smirnov'] = {'error': str(e)}
    
    # Prueba de D'Agostino-Pearson
    if len(data_clean) >= 8:
        try:
            k2_stat, k2_p = stats.normaltest(data_clean)
            results['D\'Agostino-Pearson'] = {
                'Estadístico': round(k2_stat, 4),
                'p-valor': round(k2_p, 4),
                'Es Normal (α=0.05)': k2_p > 0.05,
                'Interpretación': 'Los datos siguen una distribución normal' if k2_p > 0.05 
                                 else 'Los datos NO siguen una distribución normal'
            }
        except Exception as e:
            results['D\'Agostino-Pearson'] = {'error': str(e)}
    
    return results


def calculate_statistics_summary(data):
    """
    Calcula un resumen estadístico completo y preciso de los datos usando métodos exactos.
    
    Métodos utilizados:
    - Media: Promedio aritmético
    - Mediana: Valor central (interpolación lineal para posiciones no enteras)
    - Moda: Valor más frecuente (puede haber múltiples modas)
    - Varianza: Fórmula con n-1 (varianza muestral) o n (poblacional)
    - Desviación Estándar: Raíz de la varianza
    - Asimetría: Momento estandarizado de tercer orden
    - Curtosis: Momento estandarizado de cuarto orden (exceso)
    - Percentiles: Método de interpolación lineal
    
    Args:
        data (pd.Series): Serie de datos
        
    Returns:
        dict: Resumen estadístico completo
    """
    if pd.api.types.is_numeric_dtype(data):
        data_clean = data.dropna()
        
        if len(data_clean) == 0:
            return {'Error': 'No hay datos válidos'}
        
        # Calcular media (exacta)
        media = float(np.mean(data_clean))
        
        # Calcular mediana (método de interpolación lineal - más preciso)
        mediana = float(np.median(data_clean))
        
        # Calcular moda(s) - puede haber múltiples
        moda_series = data_clean.mode()
        if len(moda_series) > 0:
            if len(moda_series) == 1:
                moda = float(moda_series.iloc[0])
                tipo_moda = "Unimodal"
            elif len(moda_series) == 2:
                moda = float(moda_series.iloc[0])  # Primera moda
                tipo_moda = "Bimodal"
            else:
                moda = float(moda_series.iloc[0])  # Primera moda
                tipo_moda = "Multimodal"
        else:
            moda = None
            tipo_moda = "Sin moda"
        
        # Varianza y desviación estándar MUESTRAL (n-1) - más preciso
        varianza = float(np.var(data_clean, ddof=1))  # ddof=1 para muestral
        desv_std = float(np.std(data_clean, ddof=1))
        
        # Varianza y desviación estándar POBLACIONAL (n) - para referencia
        varianza_pob = float(np.var(data_clean, ddof=0))
        desv_std_pob = float(np.std(data_clean, ddof=0))
        
        # Coeficiente de variación (en porcentaje)
        cv = (desv_std / media * 100) if media != 0 else 0
        
        # Valores extremos
        minimo = float(data_clean.min())
        maximo = float(data_clean.max())
        rango = maximo - minimo
        
        # Cuartiles usando el método exclusivo (R type 7) - más estándar
        q1 = float(data_clean.quantile(0.25, interpolation='linear'))
        q2 = mediana  # Q2 es la mediana
        q3 = float(data_clean.quantile(0.75, interpolation='linear'))
        iqr = q3 - q1  # Rango intercuartílico
        
        # Percentiles adicionales
        p10 = float(data_clean.quantile(0.10, interpolation='linear'))
        p90 = float(data_clean.quantile(0.90, interpolation='linear'))
        
        # Asimetría (skewness) - método más robusto
        asimetria = float(stats.skew(data_clean, bias=False))  # bias=False para corrección muestral
        
        # Curtosis (kurtosis) - exceso de curtosis (Fisher)
        curtosis = float(stats.kurtosis(data_clean, bias=False, fisher=True))
        
        # Error estándar de la media
        error_estandar = desv_std / np.sqrt(len(data_clean))
        
        # Intervalos de confianza 95% para la media
        from scipy import stats as sp_stats
        confianza = 0.95
        grados_libertad = len(data_clean) - 1
        t_critico = sp_stats.t.ppf((1 + confianza) / 2, grados_libertad)
        margen_error = t_critico * error_estandar
        ic_inferior = media - margen_error
        ic_superior = media + margen_error
        
        # Media armónica (solo para valores positivos)
        if (data_clean > 0).all():
            media_armonica = float(stats.hmean(data_clean))
        else:
            media_armonica = None
        
        # Media geométrica (solo para valores positivos)
        if (data_clean > 0).all():
            media_geometrica = float(stats.gmean(data_clean))
        else:
            media_geometrica = None
        
        # Coeficiente de variación de Pearson
        cv_pearson = (desv_std / media) if media != 0 else None
        
        # Interpretación de asimetría
        if asimetria > 1:
            interp_asim = "Fuertemente asimétrica positiva (cola derecha)"
        elif asimetria > 0.5:
            interp_asim = "Moderadamente asimétrica positiva"
        elif asimetria > -0.5:
            interp_asim = "Aproximadamente simétrica"
        elif asimetria > -1:
            interp_asim = "Moderadamente asimétrica negativa"
        else:
            interp_asim = "Fuertemente asimétrica negativa (cola izquierda)"
        
        # Interpretación de curtosis
        if curtosis > 1:
            interp_curt = "Leptocúrtica (más puntiaguda que normal)"
        elif curtosis < -1:
            interp_curt = "Platicúrtica (más plana que normal)"
        else:
            interp_curt = "Mesocúrtica (similar a normal)"
        
        return {
            # Medidas de tendencia central
            'N (tamaño)': len(data_clean),
            'Media': round(media, 4),
            'Mediana': round(mediana, 4),
            'Moda': round(moda, 4) if moda is not None else 'Sin moda',
            'Tipo de Moda': tipo_moda,
            'Media Armónica': round(media_armonica, 4) if media_armonica is not None else 'N/A (valores ≤ 0)',
            'Media Geométrica': round(media_geometrica, 4) if media_geometrica is not None else 'N/A (valores ≤ 0)',
            
            # Medidas de dispersión
            'Varianza Muestral': round(varianza, 4),
            'Desviación Estándar Muestral': round(desv_std, 4),
            'Varianza Poblacional': round(varianza_pob, 4),
            'Desviación Estándar Poblacional': round(desv_std_pob, 4),
            'Coeficiente de Variación (%)': round(cv, 2),
            'Error Estándar': round(error_estandar, 4),
            
            # Valores extremos y rango
            'Mínimo': round(minimo, 4),
            'Máximo': round(maximo, 4),
            'Rango': round(rango, 4),
            
            # Cuartiles y percentiles
            'Q1 (Percentil 25)': round(q1, 4),
            'Q2 (Mediana/Percentil 50)': round(q2, 4),
            'Q3 (Percentil 75)': round(q3, 4),
            'Rango Intercuartílico (IQR)': round(iqr, 4),
            'Percentil 10': round(p10, 4),
            'Percentil 90': round(p90, 4),
            
            # Forma de la distribución
            'Asimetría (Skewness)': round(asimetria, 4),
            'Interpretación Asimetría': interp_asim,
            'Curtosis (Exceso)': round(curtosis, 4),
            'Interpretación Curtosis': interp_curt,
            
            # Intervalo de confianza
            'IC 95% Inferior': round(ic_inferior, 4),
            'IC 95% Superior': round(ic_superior, 4),
            'Margen de Error (95%)': round(margen_error, 4)
        }
    else:
        # Para variables cualitativas
        mode_value = data.mode()[0] if not data.mode().empty else None
        value_counts = data.value_counts()
        
        return {
            'N (tamaño)': len(data),
            'Valores Únicos': data.nunique(),
            'Moda': mode_value,
            'Frecuencia de la Moda': value_counts.iloc[0] if not value_counts.empty else 0,
            'Proporción de la Moda': round(value_counts.iloc[0] / len(data), 4) if not value_counts.empty else 0,
            'Entropía': round(-sum((value_counts/len(data)) * np.log2(value_counts/len(data))), 4)
        }
