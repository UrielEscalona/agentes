import streamlit as st
from graph.graph import app

st.title("🩺 Agente Médico Inteligente")

pregunta = st.text_input("Haz tu pregunta médica:")

if st.button("Consultar"):
    with st.spinner("Consultando base de conocimiento y generando respuesta..."):
        respuesta = app.invoke({"pregunta": pregunta})
    st.write("### Respuesta:")
    st.write(respuesta.get("generacion"))
