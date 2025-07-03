from graph.state import GraphState
from langgraph.graph import StateGraph, END
from graph.nodes.retrieve import retrieve
from graph.nodes.generate import generate
from graph.nodes.grade_documents import grade_documents
from graph.nodes.web_search import web_search
from graph.nodes.evaluate_question import evaluate_question

from dotenv import load_dotenv
load_dotenv()

RECUPERAR = "recuperar"
GENERAR = "generar"
CALIFICAR_DOCUMENTOS="calificar_documentos"
BUSQUEDA_WEB="búsqueda_web"
EVALUAR_PREGUNTA="evaluar_pregunta"

def decidir_generar(estado):
    print("---Evaluando Documentos---")
    busqueda_web = estado["busqueda_web"]
    if busqueda_web:
        print("---Existen documentos irrelevantes para la pregunta, se hará búsqueda Web---")
        return BUSQUEDA_WEB
    else:
        return GENERAR
    
def decidir_flujo(estado):
    print("---Evaluando pregunta---")
    flujo = estado["flujo"]
    if flujo:
        print("---La pregunta es sobre diagnóstico médico, responder---")
        return RECUPERAR
    else:
        print("---La pregunta no es acerca diagnóstico médico---")
        return END


flujo = StateGraph(GraphState)


flujo.add_node(EVALUAR_PREGUNTA, evaluate_question)
flujo.set_entry_point(EVALUAR_PREGUNTA)
flujo.add_node(RECUPERAR, retrieve)
flujo.add_node(GENERAR, generate)
flujo.add_node(CALIFICAR_DOCUMENTOS, grade_documents)
flujo.add_node(BUSQUEDA_WEB, web_search)
flujo.add_conditional_edges(EVALUAR_PREGUNTA, decidir_flujo, {RECUPERAR:RECUPERAR, END:END})
flujo.add_edge(RECUPERAR, CALIFICAR_DOCUMENTOS)
flujo.add_conditional_edges(CALIFICAR_DOCUMENTOS, decidir_generar, {BUSQUEDA_WEB:BUSQUEDA_WEB, GENERAR:GENERAR})
flujo.add_edge(BUSQUEDA_WEB, GENERAR)
flujo.add_edge(GENERAR, END)

app = flujo.compile()

app.get_graph().draw_mermaid_png(output_file_path="grafo.png")
