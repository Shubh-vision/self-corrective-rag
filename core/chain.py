from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.schemas import RouteQuery, Evaluator
from config.setting import llm
from langchain_groq import ChatGroq



llm2 = ChatGroq(model="llama-3.1-8b-instant")


# Router
System = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. Otherwise, use web-search.
"""
router_prompt = ChatPromptTemplate.from_messages([
    ("system", System),
    ("human", "{question}")
])
question_router = router_prompt | llm2.with_structured_output(RouteQuery)

# Generator
generate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a smart AI assistant. Use the context to answer the question."),
    ("human", "Context:\n{context}\nQuestion:\n{question}")
])
generate_chain = generate_prompt | llm | StrOutputParser()

# Evaluator
System = """You are an evaluator.
Check:
1. Are documents relevant to the question?
2. Is the answer grounded in the documents?
3. Does the answer solve the question?

Respond strictly:
relevant: yes/no
grounded: yes/no
answer_question: yes/no
"""
  
eval_prompt = ChatPromptTemplate.from_messages([
    ("system", System),
    ("human", "Q:{question}\nDocs:{documents}\nAns:{generation}")
])
evaluator_chain = eval_prompt | llm.with_structured_output(Evaluator)

# Rewrite
rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system", "Rewrite question for better retrieval"),
    ("human", "{question}")
])
rewrite_chain = rewrite_prompt | llm2 | StrOutputParser()

# Summary
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the answer in concise bullet points."),
    ("human", "{generation}")
])
summary_chain = summary_prompt | llm2 | StrOutputParser()


#=========================LOAD CHAT SUMMARY==========================================================================

# intent_prompt = ChatPromptTemplate.from_messages([
#     ("system", """
# Classify the user query into:
# - memory → if user is asking about previous chats/history
# - normal → otherwise

# Be strict.
# """),
#     ("human", "{question}")
# ])

# intent_chain = intent_prompt | llm.with_structured_output(Intent)