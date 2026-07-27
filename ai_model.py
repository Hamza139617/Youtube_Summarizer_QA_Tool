from dotenv import load_dotenv
import os


from langchain_groq import ChatGroq


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def creating_token() ->str:
    """
    retrieving the token
    """

    load_dotenv()
    token = os.getenv("Groq_Token")


    return token

def creating_llm():
    """
    initializing the large language model
    """

    token = creating_token()

    llm = ChatGroq(
        api_key=token,
        model="llama-3.1-8b-instant",
        temperature=0.0
    )

    return llm


def creating_embedding_model():
    """
    for creating the embedding model
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding_model



def create_faiss_index(chunks, embedding_model):
    """
    Create a FAISS index from text chunks using the specified embedding model.
    """

    return FAISS.from_texts(chunks, embedding_model)

def perform_similarity_search(faiss_index, query, k: int = 3):
    """
    Search for specific queries within the embedded transcript using the FAISS index
    """

    results = faiss_index.similarity_search(query, k=k)

    return results



