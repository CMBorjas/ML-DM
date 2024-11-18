from langchain.chains import RetrievalQA

def query_campaign_history(question, retriever):
    qa_chain = RetrievalQA(retriever=retriever)
    return qa_chain.run(question)
