from typing import Dict, Any

from langchain.schema import Document
from langchain_tavily import TavilySearch
from graph.state import GraphState

web_search_tool = TavilySearch(max_results=3)

def web_search(estado: GraphState) -> Dict[str, Any]:
    print("---Realizando Búsqueda Web---")
    pregunta = estado["pregunta"]
    documentos = estado.get("documentos", None)

    resultados_tavily = web_search_tool.invoke(input={"query": pregunta})["results"]
    # print(tavily_results)
    joined_resultados_tavily = "\n".join(
        [resultado_tavily["content"] for resultado_tavily in resultados_tavily]
    )
    resultados_web = Document(page_content=joined_resultados_tavily)
    if documentos is not None:
        documentos.append(resultados_web)
    else:
        documentos = [resultados_web]
    return {"pregunta": pregunta, "documentos": documentos}
