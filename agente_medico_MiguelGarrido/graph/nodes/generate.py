from typing import Any, Dict

from graph.state import GraphState
from graph.chains.generation import generation_chain


def generate(estado: GraphState) -> Dict[str, Any]:
    print("---AGENTE GENERANDO...---")
    pregunta = estado["pregunta"]
    documentos = estado["documentos"]

    generacion = generation_chain.invoke(input={"question": pregunta, "context": documentos})
    return {"pregunta": pregunta, "documentos": documentos, "generacion": generacion}