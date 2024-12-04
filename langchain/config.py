import os
from langchain import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

# RAG Model Functions ---------------------------------------------------------------------
def get_llm():
    return OpenAI(temperature=0.7, api_key=os.getenv('OPENAI_API_KEY'))

# Vector Store Functions ------------------------------------------------------------------
def create_index(corpus_path="data/corpus/"):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(
        texts=[open(f"{corpus_path}/{file}").read() for file in os.listdir(corpus_path)],
        embedding_function=embeddings,
        persist_directory=corpus_path
    )
    vectorstore.persist()

# end of langchain/config.py ----------------------------------------------------------------