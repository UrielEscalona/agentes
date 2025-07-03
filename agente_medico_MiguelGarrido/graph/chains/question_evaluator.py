from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv

class GradeQuestion(BaseModel):
    """Asigna un score binario deacuerdo al tipo de pregunta que realiza el usuario"""
    binary_score: str = Field(
        description="Verifica si la pregunta está enfocada en el área de diagnóstico médico, sólo responderás con 'si' o 'no'."
    )


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm_evaluator = llm.with_structured_output(GradeQuestion)

system = """Eres un evaluador de las preguntas que los usuarios realizan. \n
            Evaluarás cada pregunta dependiendo si esta está relacionada al área de la medicina. \n
            Sólamente aprobarás preguntas que tengan que ver con síntomas de enfermedades o padecimientos en personas."""


evaluator_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Pregunta del usuario: {pregunta}")
    ]
)

question_evaluator = evaluator_prompt | structured_llm_evaluator
