# Chatbot con Python

-Este proyecto es un chatbot que puede ejecutarse de diferentes formas: desde consola, con interfaz en Gradio o con interfaz en Streamlit. Está basado en el uso de modelos de lenguaje proporcionados por Groq.

## Instalación de dependencias

-Antes de ejecutar cualquier script, se deben instalar las dependencias necesarias. Para ello, ejecutar el siguiente comando en la raíz del proyecto:

```bash
pip install -r requirements.tx

```
### Obtener tu Api

-Este proyecto requiere una clave de API para funcionar. Cada usuario debe obtener su propia API key en: "https://console.groq.com/keys" y genera tu api key, luego ve a la carpeta raiz de el modelo y 
modifica el .env y frente a "GROQ_API_KEY=" pega tu api key, luego estaras listo para ejecutarlo


#### Correr Chat

-Para correr el chatbot directamente en la consola, se utiliza el siguiente comando desde la carpeta raíz:

```bash
python examples\modelo1.py

```


-Para contar con una interfaz gráfica simple mediante Gradio, se ejecuta:

```bash
python examples\modelo_gradio.py

```


-Para una experiencia más completa e interactiva, se recomienda usar la interfaz de Streamlit. Se ejecuta de la siguiente forma (recomendado):

```bash
streamlit run examples\modelo_streamlit.py

```

