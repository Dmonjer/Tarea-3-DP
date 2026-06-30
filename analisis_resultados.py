import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar un estilo bonito para los gráficos
sns.set_theme(style="whitegrid")

print("Cargando el dataset sintético...")
df = pd.read_csv("dataset_sintetico_llms.csv")

# Crear una carpeta para guardar los gráficos si no existe
if not os.path.exists("graficos"):
    os.makedirs("graficos")

print("\n--- ANÁLISIS CUANTITATIVO ---")

# 1. Tasa de Cumplimiento de Formato (JSON Válido)
tasa_json = df.groupby('modelo')['json_valido'].mean() * 100
print("\nTasa de respuestas en JSON válido:")
print(tasa_json)

plt.figure(figsize=(8, 5))
ax = sns.barplot(x=tasa_json.index, y=tasa_json.values, palette="viridis")
plt.title("Cumplimiento del Formato JSON por Modelo", fontsize=14)
plt.ylabel("Porcentaje de Éxito (%)")
plt.xlabel("Modelo")
plt.ylim(0, 110)
# Añadir etiquetas en las barras
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=11)
plt.savefig("graficos/1_tasa_json.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. Longitud Promedio de los Textos Generados (Diversidad y completitud)
# Contamos la cantidad de palabras aproximada separando por espacios
df['num_palabras'] = df['texto_generado'].astype(str).apply(lambda x: len(x.split()))
longitud_promedio = df.groupby('modelo')['num_palabras'].mean()
print("\nLongitud promedio de reseñas (palabras):")
print(longitud_promedio)

plt.figure(figsize=(8, 5))
ax = sns.barplot(x='modelo', y='num_palabras', data=df, palette="plasma", errorbar=None)
plt.title("Longitud Promedio de las Reseñas por Modelo", fontsize=14)
plt.ylabel("Cantidad de Palabras Promedio")
plt.xlabel("Modelo")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.0f}", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=11)
plt.savefig("graficos/2_longitud_promedio.png", dpi=300, bbox_inches='tight')
plt.close()

# 3. Tiempos de Generación
tiempo_promedio = df.groupby('modelo')['tiempo_segundos'].mean()
print("\nTiempo promedio de generación por ejemplo (segundos):")
print(tiempo_promedio)

plt.figure(figsize=(8, 5))
ax = sns.barplot(x='modelo', y='tiempo_segundos', data=df, palette="magma", errorbar=None)
plt.title("Tiempo Promedio de Generación por Modelo", fontsize=14)
plt.ylabel("Tiempo (segundos)")
plt.xlabel("Modelo")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}s", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=11)
plt.savefig("graficos/3_tiempos_generacion.png", dpi=300, bbox_inches='tight')
plt.close()

print("\n¡Análisis completado! Se han generado los gráficos en la carpeta 'graficos/'.")
print("Estos gráficos están listos para que los uses directamente en tu presentación.")
