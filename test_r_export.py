"""
Test simple para verificar la función de exportación a R
"""
import pandas as pd
import sys
sys.path.insert(0, '/workspaces/aplicacionestadistica')

from src.export import generate_r_code

# Crear datos de prueba
data = {
    'Precio': [100, 200, 150, 300, 250, 180, 220, 190, 210, 160]
}
df = pd.DataFrame(data)

# Datos para la función
selected_column = 'Precio'
variable_type = 'Cuantitativa Continua'
frequency_table = []
measures = {
    'Media': 196.0,
    'Mediana': 200.0,
    'Moda': 100.0,
    'Varianza': 3622.22,
    'Desviación Estándar': 60.18
}
quartiles = {
    'Q1 (25%)': 160.0,
    'Q2 (50%)': 200.0,
    'Q3 (75%)': 237.5
}
data_values = df['Precio'].tolist()

# Generar código R
print("Generando código R...")
r_code = generate_r_code(df, selected_column, variable_type, frequency_table, 
                         measures, quartiles, data_values)

# Verificar que el código se generó
if r_code:
    print("✅ Código R generado exitosamente!")
    print(f"Longitud del código: {len(r_code)} caracteres")
    print("\n" + "="*60)
    print("Primeras 500 caracteres del código:")
    print("="*60)
    print(r_code[:500])
    print("\n" + "="*60)
    print("Últimas 300 caracteres del código:")
    print("="*60)
    print(r_code[-300:])
    
    # Guardar en archivo de prueba
    with open('/workspaces/aplicacionestadistica/TEST_codigo_generado.R', 'w', encoding='utf-8') as f:
        f.write(r_code)
    print("\n✅ Código guardado en TEST_codigo_generado.R")
else:
    print("❌ Error: No se generó código R")

print("\n✅ Test completado!")
