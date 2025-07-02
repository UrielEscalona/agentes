from typing import Dict, Any

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState


def grade_documents(estado: GraphState) -> Dict[str, Any]:
    """
    Determina si los documentos recuperados son relevantes para la pregunta del usuario.
    si la pregunta no es relevante, se configurará una bandera para realizar una búsqueda web.
    
    Args: 
        estado (dict): Estado actual del grafo
        
    Returns:
        estado (dict): Estado filtrando documentos irrelevantes y con búsqueda web actualizada"""
    
    print("---Verificando relevancia de documentos recuperados---")
    pregunta = estado["pregunta"]
    documentos = estado["documentos"]

    docs_filtrados = []
    busqueda_web = False
    for doc in documentos:
        score = retrieval_grader.invoke(
            input={"pregunta": pregunta,"documento": doc.page_content}
            ).binary_score
        if score == "si":
            print("---Documento relevante ---")
            docs_filtrados.append(doc)
        else:
            print("---Documento irrelevante---")
            busqueda_web = True
            continue
    return {"documentos": docs_filtrados, "pregunta": pregunta, "busqueda_web": busqueda_web}