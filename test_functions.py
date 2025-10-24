#!/usr/bin/env python3
"""Script de prueba para validar las funciones sin lanzar la interfaz Streamlit"""

import sys
import pandas as pd
import numpy as np

print("=" * 60)
print(" 🧪 PRUEBAS DE FUNCIONES - Análisis Estadístico v2.0")
print("=" * 60)

# Importar módulos
print("\n1️⃣ Importando módulos...")
try:
    from src import utils, analysis, visualization
    print("   ✅ Módulos importados correctamente")
except ImportError as e:
    print(f"   ❌ Error al importar módulos: {e}")
    sys.exit(1)

# Probar detección de tipo de variable
print("\n2️⃣ Probando detección de tipo de variable...")
try:
    # Datos cualitativos
    data_cual = pd.Series(['Rojo', 'Verde', 'Azul', 'Rojo', 'Verde', 'Rojo', 'Azul', 'Verde'])
    tipo1 = utils.determine_variable_type(data_cual)
    print(f"   ✅ Cualitativa detectada: '{tipo1}'")
    assert tipo1 == "Cualitativa", f"Esperaba 'Cualitativa' pero obtuve '{tipo1}'"
    
    # Datos discretos (pocos valores enteros)
    data_disc = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5, 1, 2, 3])
    tipo2 = utils.determine_variable_type(data_disc)
    print(f"   ✅ Discreta detectada: '{tipo2}'")
    assert tipo2 in ["Cuantitativa Discreta", "Cuantitativa Discreta con Intervalos"]
    
    # Datos continuos (decimales)
    data_cont = pd.Series([1.5, 2.3, 2.8, 3.1, 3.9, 4.2, 5.7, 6.1, 7.4, 8.9])
    tipo3 = utils.determine_variable_type(data_cont)
    print(f"   ✅ Continua detectada: '{tipo3}'")
    assert tipo3 == "Cuantitativa Continua"
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar cálculos estadísticos precisos
print("\n3️⃣ Probando cálculos estadísticos precisos...")
try:
    data_test = pd.Series([10, 20, 20, 30, 30, 30, 40, 40, 50, 150])
    
    stats = analysis.calculate_statistics_summary(data_test)
    print(f"   ✅ Estadísticas calculadas: {len(stats)} medidas")
    print(f"      • Media: {stats.get('Media', 'N/A')}")
    print(f"      • Mediana: {stats.get('Mediana', 'N/A')}")
    print(f"      • Moda: {stats.get('Moda', 'N/A')}")
    print(f"      • Desviación Estándar: {stats.get('Desviación Estándar', 'N/A')}")
    print(f"      • Asimetría: {stats.get('Asimetría (Skewness)', 'N/A')}")
    print(f"      • Curtosis: {stats.get('Curtosis (Kurtosis)', 'N/A')}")
    
    # Verificar que los valores son numéricos
    assert isinstance(stats.get('Media'), (int, float))
    assert isinstance(stats.get('Mediana'), (int, float))
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar detección de outliers
print("\n4️⃣ Probando detección de outliers...")
try:
    data_outliers = pd.Series([10, 12, 11, 13, 12, 11, 14, 13, 100, 11, 12])  # 100 es outlier
    
    # IQR method
    outliers_iqr = analysis.detect_outliers_iqr(data_outliers)
    print(f"   ✅ Método IQR:")
    print(f"      • Outliers detectados: {outliers_iqr['Número de Outliers']}")
    print(f"      • Valores: {outliers_iqr['Valores Atípicos']}")
    print(f"      • IQR: {outliers_iqr['IQR']}")
    print(f"      • Límites: [{outliers_iqr['Límite Inferior']}, {outliers_iqr['Límite Superior']}]")
    
    # Z-Score method
    outliers_z = analysis.detect_outliers_zscore(data_outliers)
    print(f"   ✅ Método Z-Score:")
    print(f"      • Outliers detectados: {outliers_z['Número de Outliers']}")
    print(f"      • Valores: {outliers_z['Valores Atípicos']}")
    
    assert outliers_iqr['Número de Outliers'] > 0, "Debería detectar al menos 1 outlier"
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar tabla de frecuencia
print("\n5️⃣ Probando tabla de frecuencia...")
try:
    data_freq = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5])
    tipo = utils.determine_variable_type(data_freq)
    
    freq_table = analysis.calculate_frequency_table(data_freq, tipo)
    print(f"   ✅ Tabla generada: {len(freq_table)} filas")
    print(f"      • Tipo de variable: {tipo}")
    print(f"      • Primeras 3 filas:")
    for i, row in enumerate(freq_table[:3]):
        print(f"        {i+1}. {row}")
    
    assert len(freq_table) > 0, "La tabla debe tener al menos una fila"
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar test de normalidad
print("\n6️⃣ Probando tests de normalidad...")
try:
    # Datos aproximadamente normales
    np.random.seed(42)
    data_normal = pd.Series(np.random.normal(50, 10, 100))
    
    normality_tests = analysis.test_normality(data_normal)
    print(f"   ✅ Tests realizados:")
    for test_name, result in normality_tests.items():
        if 'error' in result:
            print(f"      • {test_name}: Error - {result['error']}")
        else:
            print(f"      • {test_name}:")
            print(f"        - Estadístico: {result['Estadístico']:.4f}")
            print(f"        - p-valor: {result['p-valor']:.4f}")
            print(f"        - ¿Normal?: {result.get('Es Normal (α=0.05)', 'N/A')}")
    
    assert 'Shapiro-Wilk' in normality_tests
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar correlación
print("\n7️⃣ Probando análisis de correlación...")
try:
    # Crear datos correlacionados
    np.random.seed(42)
    data_corr = pd.DataFrame({
        'Variable1': np.random.randn(50),
        'Variable2': np.random.randn(50),
        'Variable3': np.random.randn(50)
    })
    data_corr['Variable4'] = data_corr['Variable1'] * 2 + np.random.randn(50) * 0.1  # Altamente correlacionada
    
    corr_matrix = analysis.calculate_correlation_matrix(data_corr)
    print(f"   ✅ Matriz de correlación generada: {corr_matrix.shape}")
    print(f"      Correlación entre Variable1 y Variable4: {corr_matrix.loc['Variable1', 'Variable4']:.4f}")
    
    assert corr_matrix.shape[0] == 4
    assert corr_matrix.shape[1] == 4
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Probar con el dataset de ejemplo
print("\n8️⃣ Probando con dataset de ejemplo (ejemplo_ventas.csv)...")
try:
    df = pd.read_csv('data/ejemplo_ventas.csv')
    print(f"   ✅ Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(f"      Columnas: {list(df.columns)}")
    
    # Analizar una columna numérica
    if 'Precio' in df.columns:
        precio = df['Precio'].dropna()
        tipo_precio = utils.determine_variable_type(precio)
        print(f"   ✅ Tipo de 'Precio': {tipo_precio}")
        
        stats_precio = analysis.calculate_statistics_summary(precio)
        print(f"      • Media: {stats_precio.get('Media', 'N/A')}")
        print(f"      • Mediana: {stats_precio.get('Mediana', 'N/A')}")
    
    # Analizar una columna categórica
    if 'Categoria' in df.columns:
        categoria = df['Categoria'].dropna()
        tipo_categoria = utils.determine_variable_type(categoria)
        print(f"   ✅ Tipo de 'Categoria': {tipo_categoria}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 60)
print("\n💡 La aplicación está lista para usar. Ejecuta:")
print("   streamlit run app.py")
print("=" * 60)
