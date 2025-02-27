from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

class AnalysisRequest(BaseModel):
    review_id: str = Field(..., description="Unique identifier for the review")
    review_text: str = Field(..., description="The full text of the review")

    @field_validator('review_text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise PydanticCustomError('empty_text', 'Review Text must not be empty')
        return v

    @field_validator('review_id')
    def id_must_not_be_empty(cls, v):
        if not v.strip():
            raise PydanticCustomError('empty_id', 'Review ID must not be empty')
        return v

class Sentiment(str, Enum):
    negative = "NEGATIVE"
    positive = "POSITIVE"

class AnalysisResult(BaseModel):
    label: Sentiment
    score: float

    @field_validator('score')
    def probability_between_0_and_1(cls, v):
        if not 0 <= v <= 1:
            raise PydanticCustomError('not_in_range', 'Score must be between 0 and 1')
        return v

class AnalysisResponse(BaseModel):
    review_id: str
    details: AnalysisResult