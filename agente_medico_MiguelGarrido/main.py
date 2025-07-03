from dotenv import load_dotenv
from graph.graph import app

load_dotenv()


if __name__ == "__main__":
    pregunta_medicina = "presento fatiga, debilidad, dificultad para respirar, entumecimiento y hormigueo en las manos o pies, y edema (hinchazón) en piernas y tobillos"
    pregunta_no_relacionada = "¿Quién es el mejor jugador de futbol del mundo, Messi o CR7?"
    print("---Agente Médico---")
    pregunta = pregunta_no_relacionada
    respuesta_llm = app.invoke(
        input={
            "pregunta": pregunta
        }
    )

    print(respuesta_llm.get("generacion"))
    

