from typing import Dict, Any
from graph.chains.question_evaluator import question_evaluator
from graph.state import GraphState

def evaluate_question(estado: GraphState) -> Dict[str, Any]:
    print("---Evaluando pregunta---")
    pregunta = estado["pregunta"]
    generacion = ""

    score = question_evaluator.invoke(
        input={
            "pregunta": pregunta
        }
    )
    flujo = True
    if score.binary_score == "no":
        generacion = "Pregunta no relacionada a la medicina o diagnóstico médico"
        flujo = False
    return {"pregunta": pregunta, "generacion": generacion, "flujo": flujo, "documentos": [], "busqueda_web": False}