from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from tqdm import tqdm

from dotenv import load_dotenv

load_dotenv()

from chromadb.config import Settings

settings = Settings(anonymized_telemetry=False)

# modelo de embeddings que se utilizará
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

books = ["medicine_book1.pdf",
         "medicine_book2.pdf"] # base de conocimiento
docs = [PyPDFLoader(book).load() for book in books] # cargar los libros

docs_list = [doc for book in docs for doc in book] # obtener documentos 
# print("Número de libros cargados:", len(docs)) 
print("Número total de documentos", len(docs_list)) # cada documento es una página

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=100
) # Se define el text splitter

doc_splits = text_splitter.split_documents(docs_list) # Se separan los documentos
print("Número de documentos después de separarlos", len(doc_splits))


batch_size = 32

# Se crea el vectorstore  y se agregan los documentos por batches
vectorstore = Chroma.from_documents(
    documents=doc_splits[:batch_size],
    collection_name="rag-chroma",
    embedding=embedding_model,
    persist_directory="./.chroma",
    client_settings=settings
)

for i in tqdm(range(batch_size, len(doc_splits), batch_size)):
    batch = doc_splits[i:i+batch_size]
    vectorstore.add_documents(documents=batch)
