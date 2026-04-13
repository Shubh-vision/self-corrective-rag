from dotenv import load_dotenv
load_dotenv()

import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# ================================
# INIT PINECONE
# ================================
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_secret(key):
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key)

pc = Pinecone(api_key=get_secret("PINECONE_API_KEY"))

INDEX_NAME = "hybrid-search-langchain-pinecone"

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(INDEX_NAME)

# ================================
# INIT LLM + EMBEDDINGS
# ================================
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ================================
# VECTOR STORE (ONLY CONNECT)
# ================================
vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})