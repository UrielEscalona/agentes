# 🩺 Agente Médico

Agente Médico prototipo para curso de Agentes de IA (Actumlogos).

---

## 🚀 Configuración

### 1. Clona el repositorio

```bash
git clone -b estudiantes https://github.com/MiguelGarridoCastaneda/agentes.git
``` 

### 2. Instalar Poetry

Dirigete a la página oficial de Poetry (https://python-poetry.org/docs/#installing-with-the-official-installer) e instarla la versión compatible con tu SO.

### 3. Dirígete a la carpeta del proyecto:
```bash
cd agentes/agente_medico_MiguelGarrido
```
### 4. Instala las dependencias.
```bash
poetry install
```
### 5. Configura las variables de entorno necesarias.
Se utilizan las APIs de openai y tavily para el funcionamiento del código, así como la API de langsmith para el monitoreo (opcional). Por lo que es necesario crear un archivo .env para almacenar las API_KEYs.
```bash
OPENAI_API_KEY=<tu-apikey-de-openai>
TAVILY_API_KEY=<tu-apikey-de-tavily>
LANGSMITH_API_KEY=<tu-apikey-de-langsmith>
LANGSMITH_TRACING=true
LANGCHAIN_PROJECT=<nombre-de-proyecto>
```



## 💻 Ejecución
Puedes ejecutar el código con el siguiente comando
```bash
streamlit run interfaz.py
```
