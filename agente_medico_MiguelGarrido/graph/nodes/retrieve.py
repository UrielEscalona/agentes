from typing import Any, Dict

from graph.state import GraphState
from retrieval import retriever

def retrieve(estado: GraphState) -> Dict[str, Any]:
    print("---aplicando RAG---")
    pregunta = estado["pregunta"]

    documentos = retriever.invoke(pregunta)
    return {"pregunta": pregunta, "documentos": documentos}

