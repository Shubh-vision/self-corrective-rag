from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document
from core.schemas import Evaluator


class GraphState(TypedDict):
    question: str
    documents: List[Document]
    generation: str
    evaluation: Evaluator
    feedback: str
    summary: str
    user_id: str
