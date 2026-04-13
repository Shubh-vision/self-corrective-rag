from config.setting import retriever
import os
from core.chain import *
from core.helper import format_docs
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document
from langchain_groq import ChatGroq


# Load API key (Streamlit OR local)
try:
    import streamlit as st
    tavily_api = st.secrets["TAVILY_API_KEY"]
except:
    tavily_api = os.getenv("TAVILY_API_KEY")

# Set environment variable (IMPORTANT for Tavily)
os.environ["TAVILY_API_KEY"] = tavily_api

web_tool = TavilySearchResults(k=3)
llm = ChatGroq(model="llama-3.1-8b-instant")

# ROUTE Decision
def route(state):
    decision = question_router.invoke({"question": state['question']})
    return decision.datasource

# RETRIEVE
def retrieve(state):
    return {"documents": retriever.invoke(state['question'])}

# WEB SEARCH
def web_search(state):
    results = web_tool.invoke({"query": state['question']})
    content = "\n".join([r["content"] for r in results])
    return {"documents": [Document(page_content=content)]}

# GENERATE
def generate(state):
    return {
        "generation": generate_chain.invoke({
            "context": format_docs(state['documents']),
            "question": state['question']
        })
    }

# EVALUATE
def evaluate(state):
    result = evaluator_chain.invoke({
        "question": state['question'],
        "documents": format_docs(state['documents']),
        "generation": state['generation']
    })
    return {"evaluation": result}

# REWRITE
def rewrite(state):
    return {
        "question": rewrite_chain.invoke({
            "question": state['question']
        })
    }