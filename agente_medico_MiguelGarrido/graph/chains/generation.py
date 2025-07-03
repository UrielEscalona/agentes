from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

generation_chain = prompt | llm | StrOutputParser()