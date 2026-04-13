from pydantic import BaseModel
from typing import Literal


class RouteQuery(BaseModel):
    datasource: Literal['vectorstore', 'web_search']

class Evaluator(BaseModel):
    relevant: str
    grounded: str
    answer_question: str
