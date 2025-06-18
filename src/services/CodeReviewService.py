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

    def review_code(self, code):
        prompt = f"""
        You are an expert code reviewer. Review the following code and provide feedback on its quality, potential issues, and suggestions for improvement.
        Your response should be structured and include the following sections:
        1. Overall_Review (Should be a string)
        2. Positives (Should be a list of strings)
        3. Negatives (If any) (Should be a list of strings)
        4. Suggestions (Should be a list of strings)
        5. Score (out of 100)
        Code:
        {code}

        Please provide your feedback in a structured format.
        Response must be a JSON string that must be convertible to JSON object without modifications.
        Strictly no other information apart from the above mentioned sections should be present.
        The response should be inside curly braces without any leading or trailing characters
        """
        response = self.llm.invoke(prompt)
        return response