# 🧠 Agentes en Python

Este repositorio contiene **agentes desarrollados en Python**, mostrando cómo interactuar con modelos como los de OpenAI para tareas básicas de conversación, respuesta automática y generación de texto.

Actualmente, se incluye un agente de ejemplo basado en clonacion de voz:

```
cloador_de_voz.ipynb
```

Este archivo muestra cómo utilizar `TTS` para clonar una voz usando una muestra pequeña y poder 'decir' un texto con la voz clonada

---

## 🚀 Cómo usarlo

1. Clona el repositorio:

```bash
git clone https://github.com/UrielEscalona/agentes.git
cd agentes
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Descarga los elementos necesarios para el uso del clonador

5. Ejecuta el agente:

```bash
python clonador_de_voz.ipynb
```

---

## 🛠️ ¿Qué viene?

Este repositorio se encuentra en expansión. Se agregarán más agentes como:

- Agentes de reglas (rule-based)
- Agentes con LangChain y RAG
- Agentes colaborativos con CrewAI
- Agentes para tareas específicas (traducción, planificación, recomendación, etc.)

---

## 🤝 Contribuciones

¡Son bienvenidas! Si deseas agregar tu propio agente:

1. Haz un fork del proyecto.
2. Crea tu rama: `git checkout -b feature/mi-agente`.
3. Agrega tu script y documentación.
4. Envía un Pull Request.

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

---
