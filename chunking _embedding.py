from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.schema import Document
import os
from dotenv import load_dotenv

with open("data.txt", "r", encoding="utf-8") as file:
    data = file.read()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap = 50
)
load_dotenv(dotenv_path=r"C:\Users\HP\Desktop\rag_project\file.env")
open_ai_key = os.getenv("OPEN_AI_KEY")
chunks = splitter.split_text(data)

embeddings = OpenAIEmbeddings(
    api_key= open_ai_key
)

docs = [Document(page_content=c, metadata={"chunk_id": i}) for i, c in enumerate(chunks)]
vector_store = Chroma(
    collection_name="project",
    embedding_function=embeddings,
    persist_directory='legal'
)

batch_size = 5000
for i in range(0, len(docs), batch_size):
    batch_docs = docs[i:i + batch_size]
    vector_store.add_documents(batch_docs)

vector_store.persist()
