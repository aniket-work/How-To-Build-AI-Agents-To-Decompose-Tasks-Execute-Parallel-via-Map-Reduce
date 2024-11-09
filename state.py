from typing import Annotated, TypedDict
import operator


class OverallState(TypedDict):
    input: str
    considerations: str
    solutions: Annotated[list[str], operator.add]
    reviews: Annotated[list[str], operator.add]
    deep_thoughts: Annotated[list[str], operator.add]
    ranked_solutions: str


class SolutionState(TypedDict):
    solution: str