from langgraph.constants import END
from langgraph.graph import StateGraph

from src.Models.agent_state import AgentState
from src.services.pull_request_review_service import PullRequestReviewService

class PrReviewWorkFlow:
    def __init__(self):
        self.pullRequestReviewService = PullRequestReviewService()
        self.workflow = StateGraph(AgentState)
        self.workflow.add_node("analyze",self.pullRequestReviewService.analyze_code_changes)
        self.workflow.add_node("suggest", self.pullRequestReviewService.generate_suggestions)
        self.workflow.add_node("review", self.pullRequestReviewService.generate_review)
        self.workflow.add_node("format", self.pullRequestReviewService.format_review)
        self.workflow.set_entry_point("analyze")
        self.workflow.add_edge("analyze", "suggest")
        self.workflow.add_edge("suggest", "review")
        self.workflow.add_edge("review", "format")
        self.workflow.add_edge("format", END)
        self.engine = self.workflow.compile()