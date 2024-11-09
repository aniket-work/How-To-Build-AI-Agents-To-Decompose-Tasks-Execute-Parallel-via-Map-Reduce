from typing import List
from pydantic import BaseModel, Field


class Solutions(BaseModel):
    solutions: List[str] = Field(description="List of three solution descriptions")


class Review(BaseModel):
    review: str = Field(description="Detailed review of the solution")


class DeepThought(BaseModel):
    deep_thought: str = Field(description="Deep analysis of the solution")


class RankedSolutions(BaseModel):
    ranked_solutions: str = Field(description="Ranked solutions with justifications")