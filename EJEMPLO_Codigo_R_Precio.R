# ============================================================
# Análisis Estadístico en R - EJEMPLO
# Variable: Precio
# Tipo: Cuantitativa Continua
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
datos <- c(1200.50, 25.99, 89.99, 350.00, 75.50, 1200.50, 25.99, 89.99, 350.00, 75.50, 1200.50, 25.99, 89.99, 350.00, 75.50, 1200.50, 25.99, 89.99, 350.00, 75.50)

# Convertir a data frame
df <- data.frame(
  Precio = datos
)

# Ver primeras observaciones
head(df)

# Resumen básico
summary(df$Precio)

# ============================================================
# TABLA DE FRECUENCIAS
# ============================================================

# Para variables continuas, crear intervalos
n <- length(df$Precio)

# Calcular número de intervalos (Regla de Sturges)
k <- ceiling(1 + 3.322 * log10(n))

# Crear intervalos
intervalos <- cut(df$Precio, breaks = k, include.lowest = TRUE)

# Tabla de frecuencias
tabla_freq <- table(intervalos)
print("Frecuencias Absolutas por Intervalo:")
print(tabla_freq)

# Frecuencias relativas
tabla_rel <- prop.table(tabla_freq)
print("Frecuencias Relativas:")
print(round(tabla_rel, 4))

# Frecuencias porcentuales
tabla_porc <- prop.table(tabla_freq) * 100
print("Frecuencias Porcentuales:")
print(round(tabla_porc, 2))


# ============================================================
# MEDIDAS ESTADÍSTICAS
# ============================================================

# Medidas de tendencia central
media <- mean(df$Precio, na.rm = TRUE)
mediana <- median(df$Precio, na.rm = TRUE)

print(paste("Media:", round(media, 4)))
print(paste("Mediana:", round(mediana, 4)))

# Moda (valor más frecuente)
tabla_valores <- table(df$Precio)
moda <- as.numeric(names(tabla_valores)[which.max(tabla_valores)])
print(paste("Moda:", moda))

# Medidas de dispersión
varianza <- var(df$Precio, na.rm = TRUE)
desv_std <- sd(df$Precio, na.rm = TRUE)
rango <- max(df$Precio, na.rm = TRUE) - min(df$Precio, na.rm = TRUE)

print(paste("Varianza:", round(varianza, 4)))
print(paste("Desviación Estándar:", round(desv_std, 4)))
print(paste("Rango:", round(rango, 4)))

# Coeficiente de variación
cv <- (desv_std / media) * 100
print(paste("Coeficiente de Variación:", round(cv, 2), "%"))

# Valores mínimo y máximo
print(paste("Mínimo:", min(df$Precio, na.rm = TRUE)))
print(paste("Máximo:", max(df$Precio, na.rm = TRUE)))

# ============================================================
# CUARTILES
# ============================================================

# Calcular cuartiles
Q1 <- quantile(df$Precio, 0.25, na.rm = TRUE)
Q2 <- quantile(df$Precio, 0.50, na.rm = TRUE)  # Mediana
Q3 <- quantile(df$Precio, 0.75, na.rm = TRUE)

print(paste("Q1 (Primer Cuartil):", round(Q1, 4)))
print(paste("Q2 (Segundo Cuartil/Mediana):", round(Q2, 4)))
print(paste("Q3 (Tercer Cuartil):", round(Q3, 4)))

# Rango intercuartílico
IQR_valor <- IQR(df$Precio, na.rm = TRUE)
print(paste("Rango Intercuartílico (IQR):", round(IQR_valor, 4)))


# ============================================================
# VISUALIZACIONES
# ============================================================

# Histograma
ggplot(df, aes(x = Precio)) +
  geom_histogram(fill = "steelblue", color = "black", bins = 30) +
  labs(title = "Histograma de Precio",
       x = "Precio",
       y = "Frecuencia") +
  theme_minimal()

# Boxplot (diagrama de caja)
ggplot(df, aes(y = Precio)) +
  geom_boxplot(fill = "lightblue", color = "black") +
  labs(title = "Boxplot de Precio",
       y = "Precio") +
  theme_minimal()

# Gráfico de densidad
ggplot(df, aes(x = Precio)) +
  geom_density(fill = "steelblue", alpha = 0.5) +
  labs(title = "Densidad de Precio",
       x = "Precio",
       y = "Densidad") +
  theme_minimal()

# Q-Q Plot (para verificar normalidad)
qqnorm(df$Precio, main = "Q-Q Plot")
qqline(df$Precio, col = "red")


# ============================================================
# RESULTADOS OBTENIDOS (del análisis en Python)
# ============================================================

# Medidas de resumen calculadas:
# Media: 331.4950
# Mediana: 82.7450
# Moda: 1200.5000
# Desviación Estándar: 468.3254
# Varianza: 219328.6752
# Coeficiente de Variación: 141.28%
# Mínimo: 25.9900
# Máximo: 1200.5000

# Cuartiles calculados:
# Q1 (25%): 62.6275
# Q2 (50%): 82.7450
# Q3 (75%): 450.1250
# IQR: 387.4975

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
# Desarrollado por: JOSE CAMARENA MEZA
# Fecha de generación: 24/10/2025 03:15:00
# ============================================================
