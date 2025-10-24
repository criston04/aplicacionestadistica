# ============================================================
# Análisis Estadístico en R - EJEMPLO VARIABLE CUALITATIVA
# Variable: Categoria
# Tipo: Cualitativa
# Fecha: 24/10/2025
# Generado automáticamente por Análisis Estadístico v2.0
# ============================================================

# Cargar librerías necesarias
library(ggplot2)
library(dplyr)

# ============================================================
# DATOS ORIGINALES
# ============================================================

# Ingresar los datos
datos <- c("Electronica", "Electronica", "Electronica", "Electronica", "Electronica", 
           "Ropa", "Ropa", "Ropa", "Hogar", "Hogar", "Hogar", "Hogar",
           "Alimentos", "Alimentos", "Alimentos", "Electronica", "Ropa", "Hogar")

# Convertir a data frame
df <- data.frame(
  Categoria = datos
)

# Ver primeras observaciones
head(df)

# Resumen básico
summary(df$Categoria)

# ============================================================
# TABLA DE FRECUENCIAS
# ============================================================

# Crear tabla de frecuencias
tabla_freq <- table(df$Categoria)

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


# ============================================================
# MEDIDAS ESTADÍSTICAS
# ============================================================

# Para variables cualitativas
# Frecuencia del valor más común (moda)
tabla_valores <- table(df$Categoria)
moda <- names(tabla_valores)[which.max(tabla_valores)]
freq_moda <- max(tabla_valores)

print(paste("Moda:", moda))
print(paste("Frecuencia de la moda:", freq_moda))

# Proporción de la moda
prop_moda <- freq_moda / length(df$Categoria)
print(paste("Proporción de la moda:", round(prop_moda, 4)))


# ============================================================
# VISUALIZACIONES
# ============================================================

# Gráfico de barras
ggplot(df, aes(x = Categoria)) +
  geom_bar(fill = "steelblue", color = "black") +
  labs(title = "Distribución de Categoria",
       x = "Categoria",
       y = "Frecuencia") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Gráfico de pastel
tabla_freq <- table(df$Categoria)
pie(tabla_freq, 
    main = "Distribución de Categoria",
    col = rainbow(length(tabla_freq)),
    labels = paste(names(tabla_freq), 
                  "\n", round(prop.table(tabla_freq)*100, 1), "%"))


# ============================================================
# RESULTADOS OBTENIDOS (del análisis en Python)
# ============================================================

# Medidas de resumen calculadas:
# Moda: Electronica
# Frecuencia de la moda: 6
# Proporción: 33.33%
# Total de categorías: 4

# Distribución de frecuencias:
# Electronica: 33.33%
# Hogar: 27.78%
# Ropa: 22.22%
# Alimentos: 16.67%

# ============================================================
# ANÁLISIS ADICIONAL
# ============================================================

# Tabla de frecuencias completa con porcentajes
tabla_completa <- data.frame(
  Categoria = names(tabla_freq),
  Frecuencia = as.numeric(tabla_freq),
  Porcentaje = round(as.numeric(tabla_porc), 2)
)

print("Tabla de Frecuencias Completa:")
print(tabla_completa)

# Ordenar por frecuencia descendente
tabla_ordenada <- tabla_completa[order(-tabla_completa$Frecuencia), ]
print("Categorías ordenadas por frecuencia:")
print(tabla_ordenada)

# ============================================================
# GRÁFICOS AVANZADOS
# ============================================================

# Gráfico de barras horizontal ordenado
ggplot(tabla_completa, aes(x = reorder(Categoria, Frecuencia), y = Frecuencia)) +
  geom_bar(stat = "identity", fill = "steelblue", color = "black") +
  coord_flip() +
  labs(title = "Frecuencias por Categoría (Ordenado)",
       x = "Categoría",
       y = "Frecuencia") +
  theme_minimal() +
  geom_text(aes(label = paste0(Frecuencia, " (", Porcentaje, "%)")), 
            hjust = -0.1, size = 3)

# ============================================================
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
# Para variables cualitativas, R ofrece muchas opciones de análisis:
# - Chi-cuadrado para bondad de ajuste
# - Tablas de contingencia para relaciones entre variables
# - Gráficos de barras apiladas para comparaciones
#
# Desarrollado por: JOSE CAMARENA MEZA
# Fecha de generación: 24/10/2025 03:20:00
# ============================================================
