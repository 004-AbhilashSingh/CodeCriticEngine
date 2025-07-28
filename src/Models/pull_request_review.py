from typing import TypedDict, List

class KeyFinding(TypedDict):
    issue: str
    recommendation: str

class PullRequestReview(TypedDict):
    summary: str
    key_findings: List[KeyFinding]
    suggested_improvements: List[str]
    recommendation: str