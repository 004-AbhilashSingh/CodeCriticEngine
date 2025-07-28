from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from src.Models.agent_state import AgentState
import logging

from src.services.FormattingService import FormattingService

logger = logging.getLogger('pull_request_review_service')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class PullRequestReviewService:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )

    def analyze_code_changes(self, state:AgentState) -> AgentState:
        logger.info("Analyzing code changes...")
        diff = state["diff"]
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert code reviewer. Analyze the following code diff for potential bugs, "
                    "performance issues, security vulnerabilities, code style violations, and general best practices. "
                    "Provide your analysis in a structured format, highlighting specific lines or sections. "
                    "If no issues are found, state that clearly."
                ),
                HumanMessage(content=f"Code Diff:\n{diff}"),
            ]
        )
        chain = prompt | self.llm
        response = chain.invoke({"diff": diff})
        state["analysis"] = response.content
        logger.info("Analysis complete.")
        return state

    def generate_suggestions(self, state:AgentState) -> AgentState:
        logger.info("Generating suggestions for improvements...")
        diff = state["diff"]
        analysis = state["analysis"]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Based on the following code diff and the analysis, suggest concrete improvements. "
                    "For each suggestion, refer to the specific part of the diff it addresses. "
                    "Be actionable and concise."
                ),
                HumanMessage(content=f"Code Diff:\n```diff\n{diff}\n```\n\nAnalysis:\n{analysis}")
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke({"diff": diff, "analysis": analysis})
        state["suggestions"] = response.content
        logger.info("Suggestions generated.")
        return state

    def generate_review(self, state:AgentState) -> AgentState:
        logger.info("Generating pull request review...")
        analysis = state["analysis"]
        suggestions = state["suggestions"]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Based on the provided code analysis and suggestions, write a concise and professional "
                    "pull request review. Start with a summary, then list the key findings and suggested improvements. "
                    "Conclude with a clear recommendation (e.g., 'Looks good, ready to merge' or 'Needs changes before merging')."
                    "Make sure to return the response in a nested JSON format."
                ),
                HumanMessage(content=f"Analysis:\n{analysis}\n\nSuggestions:\n{suggestions}")
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke({"analysis": analysis, "suggestions": suggestions})
        state["review"] = response.content
        logger.info("Pull request review generated.")
        return state

    def format_review(self, state:AgentState) -> AgentState:
        logger.info("Formatting the review...")
        review = state["review"]
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Format the following review into a structured JSON format with the following keys: "
                    "'summary', 'key_findings', 'suggested_improvements', 'recommendation'. "
                    "Each element of key_findings should have two keys both having string value type - issue and recommendation. "
                    "Each element of suggested_improvements should have two keys both having string value type -  file and changes "
                    "Summary and recommendation should be strings. "
                    "Ensure that each section is clear and concise."
                ),
                HumanMessage(content=review)
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke({"review": review})
        state["review"] = response.content
        logger.info("Review formatted successfully.")
        return state