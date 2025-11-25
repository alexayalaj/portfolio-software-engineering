# ================================================
# Script en R: Medidas de Tendencia Central y Combinatoria
# Autor: Alexis Oswin Ayala Juárez
# Descripción:
#   - Calcula media, mediana y moda del conjunto de datos dado.
#   - Construye una tabla de distribución de frecuencias con los mismos intervalos usados en Excel.
#   - Resuelve los problemas de combinatoria (permutaciones y combinaciones) del caso del restaurante.
# Requisitos: Base R (sin librerías adicionales).
# ================================================

# ---------------------------
# 1) Datos
# ---------------------------
datos <- c(45, 33, 96, 78, 81, 125, 52, 80, 111, 94, 67, 76, 85, 130, 115, 85, 39, 104, 66, 132)
n <- length(datos)

# ---------------------------
# 2) Medidas de tendencia central
# ---------------------------

media   <- mean(datos)     # Promedio
mediana <- median(datos)   # Valor central

# Moda estadística (puede haber más de una)
moda <- (function(x){
  tb <- table(x)
  max_f <- max(tb)
  as.numeric(names(tb)[tb == max_f])
})(datos)

cat("\n--- Medidas de tendencia central ---\n")
cat(sprintf("Cantidad de datos: %d\n", n))
cat(sprintf("Media   : %.2f\n", media))
cat(sprintf("Mediana : %.2f\n", mediana))
if(length(moda) == 1){
  cat(sprintf("Moda    : %g\n", moda))
} else {
  cat(sprintf("Moda(s) : %s (multimodal)\n", paste(moda, collapse=", ")))
}

# ---------------------------
# 3) Tabla de distribución de frecuencias (intervalos de amplitud 20)
#    Intervalos: 30–49, 50–69, 70–89, 90–109, 110–129, 130–149
# ---------------------------

breaks  <- c(30, 50, 70, 90, 110, 130, 150)   # límites para cut()
labels  <- c("30–49", "50–69", "70–89", "90–109", "110–129", "130–149")

# Asignamos cada dato a su clase; intervalos cerrados a la izquierda y abiertos a la derecha: [a, b)
clases  <- cut(datos, breaks = breaks, right = FALSE, include.lowest = TRUE, labels = labels)

# Frecuencia por clase (queda en el mismo orden que 'labels')
freq <- as.integer(table(clases))

# Límite inferior/superior y punto medio de cada clase
lim_inf <- c(30,  50,  70,  90,  110, 130)
lim_sup <- c(49,  69,  89,  109, 129, 149)
p_med   <- (lim_inf + lim_sup) / 2

# Frecuencia acumulada, relativa y porcentaje
freq_acum <- cumsum(freq)
freq_rel  <- freq / n
porcentaje <- 100 * freq_rel

tabla_frecuencias <- data.frame(
  Intervalo            = labels,
  Limite_inferior      = lim_inf,
  Limite_superior      = lim_sup,
  Punto_medio          = p_med,
  Frecuencia           = freq,
  Frecuencia_acumulada = freq_acum,
  Frecuencia_relativa  = round(freq_rel, 4),
  Porcentaje           = round(porcentaje, 2)
)

cat("\n--- Tabla de distribución de frecuencias ---\n")
print(tabla_frecuencias, row.names = FALSE)
cat(sprintf("\nTotal de frecuencias = %d (debería ser %d)\n", sum(freq), n))

# ---------------------------
# 4) Teoría combinatoria (caso del restaurante)
# ---------------------------
# a) ¿Cuántas maneras diferentes hay de ordenar a tres clientes en una mesa? -> 3! (permutaciones de 3 en 3)
formas_clientes <- factorial(3)

# b) ¿De cuántas formas se pueden asignar dos distinciones (oro y plata) entre cuatro postres? -> P(4,2) = 4! / (4-2)!
formas_premios <- factorial(4) / factorial(4 - 2)

# c) ¿Cuántas combinaciones diferentes de dos bebidas (de 5) y dos postres (de 4) se pueden ofrecer? -> C(5,2) * C(4,2)
comb_bebidas  <- choose(5, 2)
comb_postres  <- choose(4, 2)
total_combos  <- comb_bebidas * comb_postres

cat("\n--- Resultados de combinatoria ---\n")
cat(sprintf("a) Ordenar a 3 clientes: %d formas\n", formas_clientes))
cat(sprintf("b) Asignar oro y plata entre 4 postres: %d formas\n", formas_premios))
cat(sprintf("c) Combinaciones de 2 bebidas y 2 postres: %d combinaciones\n", total_combos))

# (Opcional) Si deseas un gráfico simple de barras de la tabla de frecuencias:
# barplot(tabla_frecuencias$Frecuencia, names.arg = tabla_frecuencias$Intervalo,
#         main = "Frecuencia por intervalo", xlab = "Intervalo", ylab = "Frecuencia")
