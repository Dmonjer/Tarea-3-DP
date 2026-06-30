import urllib.request
import json
import pandas as pd
import time
import os

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELOS = ["llama3", "phi3", "mistral"]
# Para pruebas puedes poner CANTIDAD_EJEMPLOS = 5, para la tarea final usa 100
CANTIDAD_EJEMPLOS = 100 

PRODUCTOS = ["Smartphone X", "Laptop Pro", "Auriculares Inalámbricos", "Smart TV 4K", "Consola de Videojuegos"]
SENTIMIENTOS = ["Positivo", "Neutro", "Negativo"]

def crear_prompt(producto, sentimiento):
    return f"""Eres un cliente que acaba de comprar un {producto}. 
Escribe una breve reseña (alrededor de 40-50 palabras) de tu experiencia de uso. El sentimiento de tu reseña DEBE ser claramente {sentimiento}.
IMPORTANTE: Debes responder ÚNICAMENTE con un objeto JSON válido con la siguiente estructura y sin ningún texto adicional:
{{
    "producto": "{producto}",
    "resena": "tu reseña aquí",
    "sentimiento": "{sentimiento}"
}}"""

resultados = []

print("Iniciando generación de datos sintéticos con Ollama...")

for modelo in MODELOS:
    print(f"\n--- Generando con modelo: {modelo} ---")
    
    # Verificar si el modelo está disponible localmente haciendo un ping o probando
    
    for i in range(CANTIDAD_EJEMPLOS):
        producto = PRODUCTOS[i % len(PRODUCTOS)]
        sentimiento = SENTIMIENTOS[i % len(SENTIMIENTOS)]
        
        prompt = crear_prompt(producto, sentimiento)
        
        # Payload para la API de Ollama
        data = {
            "model": modelo,
            "prompt": prompt,
            "format": "json", # Fuerza al modelo a usar JSON
            "stream": False,
            "options": {
                "temperature": 0.8 # Temperatura media-alta para mayor diversidad en los ejemplos
            }
        }
        
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
        
        try:
            inicio = time.time()
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                respuesta_modelo = result.get("response", "")
                
                # Intentamos verificar que sea un JSON válido internamente
                try:
                    resena_json = json.loads(respuesta_modelo)
                    texto_final = resena_json.get("resena", respuesta_modelo)
                    es_valido = True
                except json.JSONDecodeError:
                    texto_final = respuesta_modelo
                    es_valido = False
                
                resultados.append({
                    "modelo": modelo,
                    "producto": producto,
                    "sentimiento_esperado": sentimiento,
                    "texto_generado": texto_final,
                    "json_valido": es_valido,
                    "tiempo_segundos": round(time.time() - inicio, 2)
                })
            
            print(f"[{modelo}] Ejemplo {i+1}/{CANTIDAD_EJEMPLOS} generado. (Tiempo: {round(time.time() - inicio, 1)}s)")
            
        except Exception as e:
            print(f"Error generando con {modelo} en el ejemplo {i+1}: {e}")

# Guardar y consolidar los resultados
df = pd.DataFrame(resultados)
archivo_salida = "dataset_sintetico_llms.csv"
df.to_csv(archivo_salida, index=False, encoding="utf-8")
print(f"\n¡Generación completada! Se guardaron {len(df)} registros en '{archivo_salida}'.")
