# Tarea-3-DP
Aquí se encuentra la tarea final de Deep Learning

Usamos 3 modelos locales (LLaMA3, Phi3 y Mistral) corriendo con Ollama. El objetivo de la tarea es hacerlos generar reseñas de productos electrónicos con distintos sentimientos para ver cuál es mejor armando un JSON válido y qué tan coherentes son.

### Archivos
- `generar_dataset.py`: este es el script que se conecta a Ollama y le pide las respuestas a cada modelo.
- `dataset_sintetico_llms.csv`: acá quedan guardadas las reseñas y los tiempos que tomó generarlas.
