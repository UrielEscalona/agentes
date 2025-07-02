from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

settings = Settings(anonymized_telemetry=False)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small") # modelo de embeddings

# se carga el retriever con la base de datos vectorial creada
retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=embedding_model,
    client_settings=settings
).as_retriever()