#!/usr/bin/env python3
"""Test rápido para verificar la corrección del error de None en Marca de Clase"""

import pandas as pd
import numpy as np
from src import utils, analysis

print("🧪 Probando corrección del error de None en Marca de Clase...")

# Crear datos continuos que generarán intervalos
np.random.seed(42)
data = pd.Series(np.random.uniform(10, 100, 50))

print(f"✓ Datos de prueba creados: {len(data)} valores")

# Detectar tipo de variable
tipo = utils.determine_variable_type(data)
print(f"✓ Tipo detectado: {tipo}")

# Generar tabla de frecuencia (que incluye la fila de totales con None)
try:
    freq_table = analysis.calculate_frequency_table(data, tipo)
    print(f"✓ Tabla de frecuencia generada: {len(freq_table)} filas")
    
    # Verificar que hay valores None en la última fila
    ultima_fila = freq_table[-1]
    if 'Marca de Clase' in ultima_fila:
        print(f"✓ Última fila (totales): Marca de Clase = {ultima_fila['Marca de Clase']}")
    
except Exception as e:
    print(f"✗ Error al generar tabla de frecuencia: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Intentar calcular medidas agrupadas (aquí estaba el error)
try:
    measures = analysis.calculate_all_measures_grouped(freq_table)
    print(f"✓ Medidas calculadas exitosamente: {len(measures)} medidas")
    print(f"  - Media: {measures.get('Media', 'N/A')}")
    print(f"  - Mediana: {measures.get('Mediana', 'N/A')}")
    print(f"  - Moda: {measures.get('Moda', 'N/A')}")
    print(f"  - Desviación Estándar: {measures.get('Desviación Estándar (Muestral)', 'N/A')}")
    
except Exception as e:
    print(f"✗ Error al calcular medidas: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n🎉 ¡Todas las pruebas pasaron! El error está corregido.")
