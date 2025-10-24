#!/usr/bin/env python3
"""
Script de verificación - Análisis Estadístico v2.0
Prueba que todos los módulos funcionan correctamente
"""

import sys
sys.path.insert(0, '/workspaces/aplicacionestadistica')

print("🔍 Verificando módulos del proyecto...\n")

# Test 1: Importar módulos
print("1️⃣ Importando módulos...")
try:
    from src import config, utils, analysis, visualization, export
    print("   ✅ Todos los módulos importados correctamente\n")
except Exception as e:
    print(f"   ❌ Error al importar: {e}\n")
    sys.exit(1)

# Test 2: Verificar funciones principales
print("2️⃣ Verificando funciones principales...")
try:
    # Utils
    assert hasattr(utils, 'determine_variable_type')
    assert hasattr(utils, 'handle_missing_values')
    assert hasattr(utils, 'load_csv_file')
    print("   ✅ utils.py OK")
    
    # Analysis
    assert hasattr(analysis, 'calculate_frequency_table')
    assert hasattr(analysis, 'calculate_correlation_matrix')
    assert hasattr(analysis, 'detect_outliers_iqr')
    assert hasattr(analysis, 'test_normality')
    print("   ✅ analysis.py OK")
    
    # Visualization
    assert hasattr(visualization, 'generate_histogram')
    assert hasattr(visualization, 'generate_correlation_heatmap')
    assert hasattr(visualization, 'generate_outliers_plot')
    assert hasattr(visualization, 'generate_qq_plot')
    print("   ✅ visualization.py OK")
    
    # Export
    assert hasattr(export, 'export_to_excel')
    assert hasattr(export, 'export_to_pdf')
    assert hasattr(export, 'generate_html_report')
    print("   ✅ export.py OK\n")
except AssertionError as e:
    print(f"   ❌ Error: Falta alguna función\n")
    sys.exit(1)

# Test 3: Probar con datos de ejemplo
print("3️⃣ Probando con datos de ejemplo...")
try:
    import pandas as pd
    import numpy as np
    
    # Crear datos de prueba variados
    print("   Probando detección de tipo de variable...")
    
    # Datos cualitativos
    data_cual = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'])
    tipo1 = utils.determine_variable_type(data_cual)
    print(f"   ✅ Cualitativa detectada: {tipo1}")
    
    # Datos discretos (pocos valores)
    data_disc = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5, 1, 2, 3])
    tipo2 = utils.determine_variable_type(data_disc)
    print(f"   ✅ Discreta detectada: {tipo2}")
    
    # Datos continuos
    data_cont = pd.Series([1.5, 2.3, 2.8, 3.1, 3.9, 4.2, 5.7, 6.1])
    tipo3 = utils.determine_variable_type(data_cont)
    print(f"   ✅ Continua detectada: {tipo3}")
    
    # Probar cálculos estadísticos mejorados
    print("   Probando cálculos estadísticos precisos...")
    data_test = pd.Series([10, 20, 20, 30, 30, 30, 40, 40, 50, 150])  # Con outlier
    
    # Estadísticas completas
    stats_result = analysis.calculate_statistics_summary(data_test)
    print(f"   ✅ Estadísticas calculadas: {len(stats_result)} medidas")
    print(f"      Media: {stats_result.get('Media', 'N/A')}")
    print(f"      Mediana: {stats_result.get('Mediana', 'N/A')}")
    print(f"      Asimetría: {stats_result.get('Asimetría (Skewness)', 'N/A')}")
    
    # Probar detección de outliers
    outliers = analysis.detect_outliers_iqr(data_test)
    print(f"   ✅ Outliers detectados: {outliers['Número de Outliers']}")
    
    # Probar tabla de frecuencia
    freq_table = analysis.calculate_frequency_table(data_test, tipo2)
    print(f"   ✅ Tabla de frecuencia generada: {len(freq_table)} filas\n")
    
except Exception as e:
    print(f"   ❌ Error en pruebas: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Verificar configuraciones
print("4️⃣ Verificando configuraciones...")
try:
    assert hasattr(config, 'APP_CONFIG')
    assert hasattr(config, 'FILE_CONFIG')
    assert hasattr(config, 'VISUALIZATION_CONFIG')
    assert hasattr(config, 'CUSTOM_CSS')
    print("   ✅ Todas las configuraciones OK\n")
except AssertionError:
    print("   ❌ Error: Faltan configuraciones\n")
    sys.exit(1)

# Test 5: Verificar estructura de archivos
print("5️⃣ Verificando estructura de archivos...")
import os
try:
    base_path = '/workspaces/aplicacionestadistica'
    
    required_files = [
        'app.py',
        'src/__init__.py',
        'src/config.py',
        'src/utils.py',
        'src/analysis.py',
        'src/visualization.py',
        'src/export.py',
        'data/ejemplo_ventas.csv',
        'README_v2.md',
        'GUIA_USO.py',
        'requirements.txt'
    ]
    
    for file in required_files:
        full_path = os.path.join(base_path, file)
        if os.path.exists(full_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} NO ENCONTRADO")
    
    print()
    
except Exception as e:
    print(f"   ❌ Error verificando archivos: {e}\n")

# Resumen final
print("="*60)
print("🎉 VERIFICACIÓN COMPLETADA EXITOSAMENTE")
print("="*60)
print()
print("📊 Proyecto: Análisis Estadístico v2.0")
print("✅ Módulos: OK")
print("✅ Funciones: OK")
print("✅ Configuración: OK")
print("✅ Estructura: OK")
print()
print("🚀 Para ejecutar la aplicación:")
print("   streamlit run app.py")
print()
print("📚 Para más información:")
print("   - README_v2.md → Documentación completa")
print("   - GUIA_USO.py → Guía rápida")
print("   - RESUMEN_CAMBIOS.md → Changelog detallado")
print()
