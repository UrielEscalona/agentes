from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Representa el estado del grafo
    
    Atributos:
        pregunta: pregunta
        generacion: generacion de LLM
        busqueda_web: si se buscará en internet
        documentos: List de documentos
    """

    pregunta: str
    flujo: bool
    generacion: str
    busqueda_web: bool
    documentos: List[str]