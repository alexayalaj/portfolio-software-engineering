############################################################
# Probabilidad y Estadística
# FoodDelight: comparación de métodos de entrega
# Autor: Alexis Ayala
# Descripción:
#   - Compara los tiempos de entrega de dos métodos (PKTQ001, PKTQ002)
#   - Calcula medias y varianzas
#   - Calcula diferencia de medias y error estándar
#   - Construye el intervalo de confianza al 95 %
#   - Realiza prueba de hipótesis sobre la diferencia de medias
############################################################

#===========================================================
# 0. Limpieza de entorno
#===========================================================
rm(list = ls())

# Para asegurar que los resultados sean reproducibles si se
# llegara a usar aleatoriedad (no es el caso aquí, pero es buena práctica)
set.seed(123)

#===========================================================
# 1. Captura de datos
#    Tiempos de entrega en minutos
#===========================================================

# Método A: PKTQ001
pktq001 <- c(
 21, 13, 13, 33, 20, 22, 14, 22, 22, 28, 35, 30, 25, 35, 21, 20, 23, 13,
 29, 13, 16, 35, 15, 33, 20, 22, 35, 23, 35, 20, 20, 24, 23, 14, 15, 16,
 17, 22, 20, 27, 17, 19, 33, 24, 16, 23, 31, 26, 27, 15, 22, 25, 15, 16,
 23, 34, 25, 27, 26, 15, 16, 21, 22, 19, 26, 30, 21, 20, 32, 17, 24, 24,
 33, 35, 21, 16, 23, 31, 28, 17, 30, 30, 32, 29, 22, 27, 27, 33, 26, 18,
 20, 13, 34, 23, 16, 34, 22, 33, 33, 26, 28, 20, 25, 22, 35, 30, 25, 24,
 28, 18, 26, 19, 33, 23, 15, 21, 23, 14, 35, 32, 27, 15, 16, 24, 19, 30,
 35, 20, 30, 30, 29, 28, 22, 31, 30, 33, 26, 18, 20, 14, 34, 23, 16, 34,
 22, 33, 33, 26, 28, 20, 25, 22, 35, 30, 25, 24, 28, 18, 26, 19, 33, 23,
 16, 34, 15, 13, 27, 32
)

# Método B: PKTQ002
# Nota: el enunciado menciona 168 observaciones, pero en la tabla
#       visible sólo se identifican 161 valores, que son los que se usan aquí.
pktq002 <- c(
 28, 21, 18, 19, 24, 32, 29, 22, 21, 24, 34, 24, 19, 24, 14, 34, 34, 33,
 19, 16, 34, 34, 30, 35, 26, 32, 26, 17, 35, 16, 22, 14, 23, 32, 15, 14,
 18, 32, 25, 32, 31, 16, 18, 35, 23, 35, 33, 27, 30, 35, 21, 18, 31, 17,
 25, 29, 14, 14, 17, 21, 13, 22, 31, 27, 19, 32, 33, 34, 32, 32, 26, 14,
 26, 15, 27, 19, 15, 26, 28, 33, 13, 23, 27, 25, 21, 34, 32, 16, 26, 21,
 23, 20, 17, 27, 27, 32, 18, 19, 19, 27, 32, 32, 32, 26, 16, 19, 19, 14,
 17, 34, 27, 19, 19, 27, 32, 32, 32, 26, 14, 26, 15, 27, 19, 15, 26, 28,
 33, 13, 23, 27, 25, 21, 34, 32, 16, 26, 21, 23, 20, 17, 27, 27, 32, 18,
 19, 19, 27, 32, 32, 33, 26, 28, 20, 25, 22, 35, 30, 25, 24, 28, 18
)

cat("Tamaño muestra PKTQ001:", length(pktq001), "\n")
cat("Tamaño muestra PKTQ002:", length(pktq002), "\n\n")

#===========================================================
# 2. Estadísticos descriptivos
#===========================================================

# Medias
mean_pktq001 <- mean(pktq001)
mean_pktq002 <- mean(pktq002)

# Varianzas muestrales
var_pktq001 <- var(pktq001)
var_pktq002 <- var(pktq002)

# Desviaciones estándar
sd_pktq001 <- sd(pktq001)
sd_pktq002 <- sd(pktq002)

cat("=== Estadísticos descriptivos ===\n")
cat("PKTQ001 -> media:", round(mean_pktq001, 2),
    " varianza:", round(var_pktq001, 2),
    " sd:", round(sd_pktq001, 2), "\n")
cat("PKTQ002 -> media:", round(mean_pktq002, 2),
    " varianza:", round(var_pktq002, 2),
    " sd:", round(sd_pktq002, 2), "\n\n")

# Resumen en data frame (útil para exportar o imprimir ordenado)
resumen <- data.frame(
  Metodo   = c("PKTQ001", "PKTQ002"),
  n        = c(length(pktq001), length(pktq002)),
  Media    = c(mean_pktq001, mean_pktq002),
  Varianza = c(var_pktq001, var_pktq002),
  SD       = c(sd_pktq001, sd_pktq002)
)

print(resumen)
cat("\n")

#===========================================================
# 3. Diferencia de medias y error estándar
#===========================================================

diff_medias <- mean_pktq001 - mean_pktq002
se_diff     <- sqrt(var_pktq001/length(pktq001) + var_pktq002/length(pktq002))

cat("=== Diferencia de medias (PKTQ001 - PKTQ002) ===\n")
cat("d̂ =", round(diff_medias, 3), "minutos\n")
cat("Error estándar SE(d̂) =", round(se_diff, 3), "minutos\n\n")

#===========================================================
# 4. Intervalo de confianza al 95 %
#===========================================================

alpha  <- 0.05
z_crit <- qnorm(1 - alpha/2)    # 1.96 para 95 %

LI <- diff_medias - z_crit * se_diff
LS <- diff_medias + z_crit * se_diff

cat("=== Intervalo de confianza al 95% para (μ1 - μ2) ===\n")
cat("LI =", round(LI, 3), "LS =", round(LS, 3), " (minutos)\n\n")

#===========================================================
# 5. Prueba de hipótesis
#    H0: μ1 = μ2   vs   H1: μ1 ≠ μ2
#===========================================================

Z <- diff_medias / se_diff
p_valor <- 2 * (1 - pnorm(abs(Z)))    # prueba bilateral

cat("=== Prueba de hipótesis bilateral ===\n")
cat("Estadístico Z =", round(Z, 3), "\n")
cat("Valor-p =", round(p_valor, 4), "\n")

# Región de rechazo para α = 0.05:
# Rechazar H0 si |Z| > 1.96
cat("Región de rechazo: |Z| > 1.96\n")

if (abs(Z) > 1.96) {
  cat("Conclusión estadística: se rechaza H0 (hay evidencia de diferencia de medias).\n")
} else {
  cat("Conclusión estadística: NO se rechaza H0 (no hay evidencia de diferencia de medias).\n")
}
cat("\n")

#===========================================================
# 6. Interpretación ejecutiva (mensaje final)
#===========================================================

if (abs(Z) > 1.96) {
  mensaje <- paste0(
    "Con un nivel de confianza del 95%, la prueba indica una diferencia ",
    "estadísticamente significativa entre los tiempos promedio de los métodos.\n",
    "Los resultados sugieren que la diferencia observada en las medias no se debe solo al azar muestral."
  )
} else {
  mensaje <- paste0(
    "Con un nivel de confianza del 95%, NO se detecta una diferencia ",
    "estadísticamente significativa entre los tiempos promedio de los métodos PKTQ001 y PKTQ002.\n",
    "Cualquier diferencia observada en esta muestra puede explicarse razonablemente por variación aleatoria."
  )
}

cat("=== Interpretación ejecutiva ===\n")
cat(mensaje, "\n")
