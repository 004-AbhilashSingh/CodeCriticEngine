import json
from tokenize import endpats


class FormattingService:
    @staticmethod
    def convert_to_json(json_string):
        start_index = json_string.find('{')
        end_index = json_string.rfind('}') + 1
        json_string = json_string[start_index:end_index]
        print(json_string)
        try:
            return json.loads(json_string)
        except Exception as e:
            return {"error": str(e)}