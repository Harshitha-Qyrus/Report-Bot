from pydantic import BaseModel
from typing import List

class MYSQL_MODEL(BaseModel):
    mysql_command: str
    
class AnswerQuestionSchema(BaseModel):
    user_description: str

class GenerateGraphAndInsights(BaseModel):
    user_description: str

class FORMAT_ANSWER(BaseModel):
    formatted_answers: str
    
class FORMAT_NUMBERED_CARD(BaseModel):
    abstract_answer:str

class GenerateGraph(BaseModel):
    graph_code: str

class GraphIdea(BaseModel):
    graph_description: str
    graph_details: str
    reason: str

class GenerateReportLayoutSchema(BaseModel):
    graphs: List[GraphIdea]
    
class QuestionsList(BaseModel):
    questions:str
    detail:str
    
class GenerateReportInsightListsSchema(BaseModel):
    insight:List[QuestionsList]

class CORRECT_JSON(BaseModel):
    corrected_json: str


