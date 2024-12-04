from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Player  # Assuming models.py defines your database models
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import json
import os

# Database connection setup
engine = create_engine('sqlite:///../data/database.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_player_profile(player_id):
    """
    Retrieve a player's profile from the database.
    """
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        return {
            "id": player.id,
            "name": player.name,
            "stats": player.stats,
            "inventory": player.inventory,
            "actions": player.actions
        }
    return None

# RAG Model Functions ---------------------------------------------------------------------
def preprocess_corpus(file_path):
    """
    Preprocess the JSON corpus and return a list of text chunks.
    """
    with open(file_path, "r") as f:
        corpus = json.load(f).get("text", [])

    # Convert JSON dialogue, actions, and choices into a string format
    processed_text = []

    def process_choice(choice_list):
        """
        Recursively process nested choices and add them to the processed text.
        """
        for sequence in choice_list:
            for line in sequence:
                key, value = list(line.items())[0]
                processed_text.append(f"{key}: {value}")

    for entry in corpus:
        if "ACTION" in entry:
            processed_text.append(f"ACTION: {entry['ACTION']}")
        elif "CHOICE" in entry:
            process_choice(entry["CHOICE"])
        else:
            for key, value in entry.items():
                processed_text.append(f"{key}: {value}")

    return processed_text

# Vector Store Functions ------------------------------------------------------------------
def create_vector_store(processed_text, index_path="../data/corpus/faiss_index"):
    """
    Create a vector store from processed text and save it.
    """
    if not os.path.exists(os.path.dirname(index_path)):
        os.makedirs(os.path.dirname(index_path))

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_text("\n".join(processed_text))
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(docs, embeddings)
    vector_store.save_local(index_path)
    return vector_store

# RAG Chain Functions ---------------------------------------------------------------------
def get_rag_chain(index_path="../data/corpus/faiss_index"):
    """
    Load the vector store and create a RAG chain.
    """
    vector_store = FAISS.load_local(index_path, OpenAIEmbeddings())
    llm = OpenAI(temperature=0.7)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever())
    return qa_chain

# Query Functions --------------------------------------------------------------------------
def query_rag_chain(query):
    """
    Query the RAG chain for a response.
    """
    chain = get_rag_chain()
    return chain.run({"query": query})

# Main Function ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Example: Preprocess corpus and create vector store
    corpus_path = "../data/corpus/campaign_data.json"
    index_path = "../data/corpus/faiss_index"

    # Step 1: Preprocess corpus and create vector store from processed ---------------------
    processed_text = preprocess_corpus(corpus_path)

    # Step 2: Create vector store from processed text ---------------------------------------
    create_vector_store(processed_text, index_path)

    # Step 3: Test the RAG chain with a query ------------------------------------------------
    test_query = "What should Tifa say next?"
    response = query_rag_chain(test_query)
    print(f"RAG Response: {response}")
