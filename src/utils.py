"""
Utilidades y funciones auxiliares para el análisis estadístico.
"""
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


def detect_and_convert_dates(data):
    """
    Detecta si una columna contiene fechas y las convierte a formato numérico.
    
    Args:
        data (pd.Series): Serie de datos a analizar
        
    Returns:
        tuple: (es_fecha: bool, datos_convertidos: pd.Series, info: dict)
    """
    if len(data.dropna()) == 0:
        return False, data, {}
    
    # Lista de formatos de fecha comunes
    date_formats = [
        '%d/%m/%Y',  # 16/04/2024
        '%d-%m-%Y',  # 16-04-2024
        '%Y-%m-%d',  # 2024-04-16 (ISO)
        '%m/%d/%Y',  # 04/16/2024 (US)
        '%d/%m/%y',  # 16/04/24
        '%d-%m-%y',  # 16-04-24
        '%Y/%m/%d',  # 2024/04/16
    ]
    
    data_clean = data.dropna().astype(str)
    
    # Intentar detectar formato de fecha
    for date_format in date_formats:
        try:
            # Intentar convertir una muestra
            sample = data_clean.iloc[0] if len(data_clean) > 0 else None
            if sample:
                datetime.strptime(sample, date_format)
                
                # Si funciona, convertir toda la serie
                dates = pd.to_datetime(data_clean, format=date_format, errors='coerce')
                valid_dates = dates.notna().sum()
                
                # Si al menos el 80% son fechas válidas
                if valid_dates / len(data_clean) >= 0.8:
                    # Convertir a días desde la primera fecha
                    min_date = dates.min()
                    days_since_start = (dates - min_date).dt.days
                    
                    info = {
                        'formato': date_format,
                        'fecha_inicial': min_date,
                        'fecha_final': dates.max(),
                        'rango_dias': days_since_start.max(),
                        'tipo_conversion': 'dias_desde_inicio'
                    }
                    
                    return True, days_since_start, info
        except:
            continue
    
    # Intentar con pd.to_datetime (más flexible)
    try:
        dates = pd.to_datetime(data_clean, errors='coerce', dayfirst=True)
        valid_dates = dates.notna().sum()
        
        if valid_dates / len(data_clean) >= 0.8:
            min_date = dates.min()
            days_since_start = (dates - min_date).dt.days
            
            info = {
                'formato': 'auto-detectado',
                'fecha_inicial': min_date,
                'fecha_final': dates.max(),
                'rango_dias': days_since_start.max(),
                'tipo_conversion': 'dias_desde_inicio'
            }
            
            return True, days_since_start, info
    except:
        pass
    
    return False, data, {}


def determine_variable_type(data):
    """
    Determina el tipo de variable basándose en los datos con análisis mejorado.
    
    Criterios de clasificación:
    - Cualitativa: Datos no numéricos o numéricos que representan categorías
    - Cuantitativa Discreta: Enteros con pocos valores únicos (≤ 20 o < 5% del total)
    - Cuantitativa Discreta con Intervalos: Enteros con muchos valores únicos
    - Cuantitativa Continua: Datos decimales o enteros con valores continuos
    
    Args:
        data (pd.Series): Serie de datos a analizar
        
    Returns:
        str: Tipo de variable detectado
    """
    # Eliminar valores nulos para análisis
    data_clean = data.dropna()
    
    if len(data_clean) == 0:
        return "Cualitativa"  # Por defecto si no hay datos
    
    # 1. Verificar si es numérico a nivel de pandas
    is_numeric_dtype = pd.api.types.is_numeric_dtype(data_clean)
    
    # 2. Intentar conversión a numérico para detectar datos mixtos
    try:
        data_numeric = pd.to_numeric(data_clean, errors='coerce')
        numeric_count = data_numeric.notna().sum()
        total_count = len(data_clean)
        
        # Si menos del 90% son numéricos, es cualitativa
        if numeric_count / total_count < 0.9:
            return "Cualitativa"
        
        # Usar los datos numéricos para análisis posterior
        data_for_analysis = data_numeric.dropna()
        
    except:
        return "Cualitativa"
    
    # 3. Si no es numérico según pandas, verificar contenido
    if not is_numeric_dtype:
        # Verificar si hay strings que no son números
        if data_clean.dtype == 'object':
            return "Cualitativa"
    
    # 4. Análisis de datos numéricos
    unique_values = data_for_analysis.nunique()
    total_values = len(data_for_analysis)
    
    # Calcular si son enteros (con tolerancia para errores de punto flotante)
    is_integer_values = np.allclose(data_for_analysis, data_for_analysis.round(), rtol=1e-9, atol=1e-9)
    
    # 5. Verificar si son valores enteros
    if is_integer_values:
        # Criterios mejorados para clasificar discretas
        ratio_unique = unique_values / total_values
        
        # Discreta si:
        # - Menos de 20 valores únicos Y
        # - Menos del 5% de valores únicos respecto al total
        if unique_values <= 20 and ratio_unique < 0.05:
            return "Cuantitativa Discreta"
        
        # Discreta también si muy pocos valores únicos sin importar el total
        elif unique_values <= 10:
            return "Cuantitativa Discreta"
        
        # Discreta con intervalos si hay muchos valores únicos pero son enteros
        else:
            # Verificar si hay un patrón de conteo (1,2,3,4...) que sugiere discreta
            data_sorted = sorted(data_for_analysis.unique())
            if len(data_sorted) > 1:
                diffs = np.diff(data_sorted)
                # Si la mayoría de diferencias son 1, probablemente es discreta con intervalos
                if np.median(diffs) == 1.0 and np.mean(diffs) <= 2.0:
                    return "Cuantitativa Discreta con Intervalos"
            
            # Si tiene muchos valores únicos pero son conteos, tratar como discreta con intervalos
            if ratio_unique > 0.5:  # Más del 50% son únicos
                return "Cuantitativa Continua"  # Probablemente IDs o algo similar
            else:
                return "Cuantitativa Discreta con Intervalos"
    
    # 6. Si llegamos aquí, son valores decimales → Continua
    else:
        # Verificar que realmente haya variación decimal
        decimal_parts = np.abs(data_for_analysis - data_for_analysis.round())
        has_decimals = (decimal_parts > 1e-10).any()
        
        if has_decimals:
            return "Cuantitativa Continua"
        else:
            # Por seguridad, si no hay decimales reales, revisar como discreta
            if unique_values <= 20:
                return "Cuantitativa Discreta"
            else:
                return "Cuantitativa Discreta con Intervalos"


def handle_missing_values(df, column, method):
    """
    Maneja los valores nulos en un DataFrame según el método especificado.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        column (str): Nombre de la columna a procesar
        method (str): Método para manejar nulos ("Eliminar", "Reemplazar por la media", etc.)
        
    Returns:
        tuple: (DataFrame procesado, mensaje de resultado)
    """
    missing_count = df[column].isna().sum()
    
    if missing_count == 0:
        return df, "No hay valores nulos en la columna."
    
    if method == "Eliminar":
        df_clean = df.dropna(subset=[column])
        return df_clean, f"Se eliminaron {missing_count} filas con valores nulos."
    
    elif method == "Reemplazar por la media":
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())
            return df, f"Se reemplazaron {missing_count} valores nulos por la media."
        else:
            return df, "Error: No se puede calcular la media para variables no numéricas."
    
    elif method == "Reemplazar por la mediana":
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].median())
            return df, f"Se reemplazaron {missing_count} valores nulos por la mediana."
        else:
            return df, "Error: No se puede calcular la mediana para variables no numéricas."
    
    elif method == "Reemplazar por cero":
        df[column] = df[column].fillna(0)
        return df, f"Se reemplazaron {missing_count} valores nulos por cero."
    
    return df, "Método no reconocido."


def prepare_data_for_correlation(df, columns_to_analyze=None):
    """
    Prepara un DataFrame para análisis de correlación, detectando y convirtiendo fechas.
    
    Args:
        df (pd.DataFrame): DataFrame original
        columns_to_analyze (list): Lista de columnas a analizar (None = todas)
        
    Returns:
        tuple: (df_numeric: pd.DataFrame, conversion_info: dict)
    """
    if columns_to_analyze is None:
        columns_to_analyze = df.columns.tolist()
    
    df_numeric = pd.DataFrame()
    conversion_info = {}
    
    for col in columns_to_analyze:
        if col not in df.columns:
            continue
        
        # Verificar si es fecha
        is_date, converted_data, date_info = detect_and_convert_dates(df[col])
        
        if is_date:
            # Es fecha, usar datos convertidos
            df_numeric[col] = converted_data
            conversion_info[col] = {
                'tipo_original': 'fecha',
                'tipo_convertido': 'numerico (días)',
                'info': date_info
            }
        else:
            # Intentar convertir a numérico
            try:
                numeric_data = pd.to_numeric(df[col], errors='coerce')
                if numeric_data.notna().sum() / len(df[col].dropna()) >= 0.8:
                    df_numeric[col] = numeric_data
                    conversion_info[col] = {
                        'tipo_original': 'numerico',
                        'tipo_convertido': 'numerico',
                        'info': {}
                    }
            except:
                # No se puede convertir, omitir
                pass
    
    return df_numeric, conversion_info


@st.cache_data
def load_csv_file(file, separator, decimal, encoding):
    """
    Carga un archivo CSV con caché.
    
    Args:
        file: Archivo subido
        separator (str): Separador de columnas
        decimal (str): Separador decimal
        encoding (str): Codificación del archivo
        
    Returns:
        pd.DataFrame: DataFrame cargado
    """
    return pd.read_csv(file, sep=separator, decimal=decimal, encoding=encoding)


@st.cache_data
def load_excel_file(file):
    """
    Carga un archivo Excel con caché.
    
    Args:
        file: Archivo subido
        
    Returns:
        pd.DataFrame: DataFrame cargado
    """
    return pd.read_excel(file)


def format_number(value, decimals=2):
    """
    Formatea un número con el número especificado de decimales.
    
    Args:
        value: Valor a formatear
        decimals (int): Número de decimales
        
    Returns:
        str: Número formateado
    """
    if value is None:
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}"
    return str(value)


def validate_dataframe(df):
    """
    Valida que el DataFrame esté correctamente formado.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        
    Returns:
        tuple: (bool: es válido, str: mensaje de error si aplica)
    """
    if df is None or df.empty:
        return False, "El DataFrame está vacío."
    
    if df.shape[0] < 1:
        return False, "El DataFrame no tiene filas."
    
    if df.shape[1] < 1:
        return False, "El DataFrame no tiene columnas."
    
    return True, "DataFrame válido."


def get_numeric_columns(df):
    """
    Obtiene las columnas numéricas de un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
        
    Returns:
        list: Lista de nombres de columnas numéricas
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df):
    """
    Obtiene las columnas categóricas de un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
        
    Returns:
        list: Lista de nombres de columnas categóricas
    """
    return df.select_dtypes(include=['object', 'category']).columns.tolist()
