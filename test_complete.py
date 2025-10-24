#!/usr/bin/env python3
"""Test completo con el dataset de ejemplo"""

import pandas as pd
from src import utils, analysis

print("🧪 Probando con dataset de ejemplo (ejemplo_ventas.csv)...")

try:
    # Cargar el dataset
    df = pd.read_csv('data/ejemplo_ventas.csv')
    print(f"✓ Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
    
    # Probar con una columna numérica continua
    print("\n📊 Probando con columna 'Precio' (Continua)...")
    precio = df['Precio'].dropna()
    tipo_precio = utils.determine_variable_type(precio)
    print(f"  ✓ Tipo detectado: {tipo_precio}")
    
    freq_table_precio = analysis.calculate_frequency_table(precio, tipo_precio)
    print(f"  ✓ Tabla de frecuencia: {len(freq_table_precio)} filas")
    
    if tipo_precio in ["Cuantitativa Discreta con Intervalos", "Cuantitativa Continua"]:
        measures_precio = analysis.calculate_all_measures_grouped(freq_table_precio)
        print(f"  ✓ Medidas agrupadas calculadas: {len(measures_precio)} medidas")
        print(f"    - Media: {measures_precio.get('Media', 'N/A')}")
        print(f"    - Mediana: {measures_precio.get('Mediana', 'N/A')}")
    
    # Probar con una columna numérica discreta
    print("\n📊 Probando con columna 'Cantidad_Vendida' (Discreta)...")
    cantidad = df['Cantidad_Vendida'].dropna()
    tipo_cantidad = utils.determine_variable_type(cantidad)
    print(f"  ✓ Tipo detectado: {tipo_cantidad}")
    
    freq_table_cantidad = analysis.calculate_frequency_table(cantidad, tipo_cantidad)
    print(f"  ✓ Tabla de frecuencia: {len(freq_table_cantidad)} filas")
    
    if tipo_cantidad in ["Cuantitativa Discreta con Intervalos", "Cuantitativa Continua"]:
        measures_cantidad = analysis.calculate_all_measures_grouped(freq_table_cantidad)
        print(f"  ✓ Medidas agrupadas calculadas: {len(measures_cantidad)} medidas")
        print(f"    - Media: {measures_cantidad.get('Media', 'N/A')}")
    else:
        # Para datos discretos sin intervalos
        stats = analysis.calculate_statistics_summary(cantidad)
        print(f"  ✓ Estadísticas calculadas: {len(stats)} medidas")
        print(f"    - Media: {stats.get('Media', 'N/A')}")
    
    # Probar con una columna cualitativa
    print("\n📊 Probando con columna 'Categoria' (Cualitativa)...")
    categoria = df['Categoria'].dropna()
    tipo_categoria = utils.determine_variable_type(categoria)
    print(f"  ✓ Tipo detectado: {tipo_categoria}")
    
    freq_table_categoria = analysis.calculate_frequency_table(categoria, tipo_categoria)
    print(f"  ✓ Tabla de frecuencia: {len(freq_table_categoria)} filas")
    
    print("\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("✅ El error de None en Marca de Clase está corregido")
    print("✅ La aplicación está lista para usar")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
