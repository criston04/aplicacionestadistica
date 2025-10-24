#!/usr/bin/env python3
"""Test de detección y conversión de fechas para correlación"""

import pandas as pd
import sys
import os

# Evitar que streamlit se inicie
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

from src.utils import detect_and_convert_dates, prepare_data_for_correlation

print("=" * 70)
print("🧪 TEST: Detección y Conversión de Fechas para Correlación")
print("=" * 70)

# Test 1: Detectar fechas en formato dd/mm/yyyy
print("\n1️⃣ Test: Detectar fechas en formato 16/04/2024...")
fechas = pd.Series([
    '16/04/2024',
    '23/04/2024',
    '30/04/2024',
    '07/05/2024',
    '14/05/2024'
])

is_date, converted, info = detect_and_convert_dates(fechas)
print(f"   ¿Es fecha?: {is_date}")
if is_date:
    print(f"   Formato detectado: {info['formato']}")
    print(f"   Fecha inicial: {info['fecha_inicial']}")
    print(f"   Fecha final: {info['fecha_final']}")
    print(f"   Rango: {info['rango_dias']} días")
    print(f"   Valores convertidos: {converted.tolist()}")
    print("   ✅ Fechas detectadas y convertidas correctamente")
else:
    print("   ❌ No se detectaron como fechas")

# Test 2: Cargar dataset de ejemplo con fechas
print("\n2️⃣ Test: Cargar dataset ejemplo_crecimiento_plantas.csv...")
try:
    df = pd.read_csv('data/ejemplo_crecimiento_plantas.csv')
    print(f"   ✅ Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(f"   Columnas: {list(df.columns)}")
    
    # Mostrar primeras filas
    print("\n   Primeras 3 filas:")
    print(df.head(3).to_string(index=False))
    
except Exception as e:
    print(f"   ❌ Error al cargar: {e}")

# Test 3: Preparar datos para correlación
print("\n3️⃣ Test: Preparar datos para correlación (convierte fechas)...")
try:
    df_prepared, conversion_info = prepare_data_for_correlation(df)
    print(f"   ✅ Datos preparados: {df_prepared.shape[0]} filas × {df_prepared.shape[1]} columnas")
    print(f"   Columnas preparadas: {list(df_prepared.columns)}")
    
    if conversion_info:
        print("\n   📋 Información de conversiones:")
        for col, info in conversion_info.items():
            print(f"\n   • {col}:")
            print(f"     - Tipo original: {info['tipo_original']}")
            print(f"     - Tipo convertido: {info['tipo_convertido']}")
            if info['tipo_original'] == 'fecha':
                print(f"     - Fecha inicial: {info['info']['fecha_inicial']}")
                print(f"     - Rango: {info['info']['rango_dias']} días")
    
    print("\n   Primeras 3 filas de datos convertidos:")
    print(df_prepared.head(3).to_string(index=False))
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Calcular correlación
print("\n4️⃣ Test: Calcular correlación con fechas convertidas...")
try:
    from src.analysis import calculate_correlation_matrix
    
    corr_matrix = calculate_correlation_matrix(df_prepared, list(df_prepared.columns))
    print(f"   ✅ Matriz de correlación calculada: {corr_matrix.shape}")
    print("\n   📊 Matriz de Correlación:")
    print(corr_matrix.round(4).to_string())
    
    # Encontrar correlación más fuerte con Fecha
    if 'Fecha' in corr_matrix.columns:
        print("\n   🔍 Correlaciones con Fecha (días transcurridos):")
        fecha_corr = corr_matrix['Fecha'].drop('Fecha').sort_values(ascending=False)
        for var, corr in fecha_corr.items():
            print(f"      • {var}: {corr:.4f}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ TESTS COMPLETADOS")
print("=" * 70)
print("\n💡 Ahora puedes usar la aplicación para analizar datos con fechas:")
print("   1. Carga el archivo: data/ejemplo_crecimiento_plantas.csv")
print("   2. Ve a la pestaña 'Análisis de Correlación'")
print("   3. Las fechas se convertirán automáticamente a días")
print("   4. Podrás ver la correlación entre fecha y largo del tallo")
print("=" * 70)
