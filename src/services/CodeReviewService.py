from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

class CodeReviewService:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )

    def test_llm(self,text):
        response = self.llm.invoke(
            text
        )
        return response

