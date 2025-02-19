from pydantic import BaseModel
from typing import Dict, List

class MentorQuery(BaseModel):
    mentor_type: str
    query: str

class ScenarioRequest(BaseModel):
    mentor_type: str
    difficulty: str

class FeedbackRequest(BaseModel):
    mentor_type: str
    scenario: str
    solution: str

class MentorResponse(BaseModel):
    mentor_name: str
    primary_response: str
    enrichment: Dict[str, str]

class ScenarioResponse(BaseModel):
    scenario: Dict[str, str]

class FeedbackResponse(BaseModel):
    feedback: Dict[str, str]