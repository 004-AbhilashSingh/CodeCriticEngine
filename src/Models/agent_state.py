from typing import TypedDict

from src.Models.pull_request_review import PullRequestReview


class AgentState(TypedDict):
    diff: str
    analysis: str
    suggestions: str
    review: str