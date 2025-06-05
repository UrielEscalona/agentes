# 🎙️ Traductor y Clonador de Voz (Español → Inglés)

Este proyecto permite traducir tu voz hablada en español al inglés y reproducir la traducción con tu propia voz clonada.

## 🧠 ¿Qué hace este sistema?
1. **Carga un archivo de audio** en formato `.wav`, `.mp3` o `.ogg`.
2. **Transcribe y traduce** el audio con el modelo `Whisper` de OpenAI usando `task="translate"`.
3. **Clona tu voz** con el modelo `XTTS` y genera un nuevo audio con la traducción en inglés pero con tu misma voz.
4. **Reproduce el audio** resultante desde la interfaz web creada con Streamlit.

## ⚠️ Nota importante sobre la traducción
Este sistema usa `Whisper` de OpenAI en modo `translate`, lo que traduce directamente del idioma original (español) al inglés. Aunque es útil para tareas rápidas, **la calidad de traducción puede no ser precisa** en frases complejas o con ambigüedad. Para traducciones de alta fidelidad, se recomienda el uso de modelos especializados como GPT o APIs externas como Google Translate.

## ✅ Formatos soportados
- `.wav`
- `.mp3`
- `.ogg`

## 🚀 Cómo ejecutar
1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta la aplicación:
```bash
streamlit run app.py
```

## 🛠️ Tecnologías utilizadas
- `Streamlit` para la interfaz web
- `Whisper` para transcripción y traducción automática
- `TTS (XTTS v2)` para clonación de voz
- `Pydub` para convertir formatos de audio

---

Este sistema es una base funcional para experimentar con traducción automática y clonación de voz. ¡Explóralo y mejóralo!