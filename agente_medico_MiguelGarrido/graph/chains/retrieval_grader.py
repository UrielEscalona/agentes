from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class GradeDocuments(BaseModel):
    """Asigna score binario deacuerdo a la relevancia de los documentos recuperados."""

    binary_score: str = Field(
        description="¿Los documentos son relevantes para la pregunta?, 'si' o 'no'"
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """Eres un evaluador que esta a cargo de calificar la relevancia del documento recuperado para una pregunta del usuario. \n
            Si el documento contiene palabras claves o significado semántico relacionado a la pregunta calificalo como relevante. \n
            Da una calificación binaria de 'si' o 'no' indicando si el documento es relevante o no a la pregunta."""


grade_prompt = ChatPromptTemplate(
    [
        ("system", system),
        ("human", "Documento recuperado: {documento} \n\n Pregunta del usuario: {pregunta}")
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader