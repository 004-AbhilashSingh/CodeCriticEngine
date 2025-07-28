import json
from tokenize import endpats


class FormattingService:
    @staticmethod
    def convert_to_json(json_string):
        start_index = json_string.find('{')
        end_index = json_string.rfind('}') + 1
        json_string = json_string[start_index:end_index]
        try:
            return json.loads(json_string)
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def convert_to_pull_request_review(review):
        try:
            return {
                "summary": review.get("summary", ""),
                "key_findings": review.get("key_findings", []),
                "suggested_improvements": review.get("suggested_improvements", []),
                "recommendation": review.get("recommendation", "")
            }
        except Exception as e:
            return {"error": str(e)}