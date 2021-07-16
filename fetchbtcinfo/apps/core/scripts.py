import json
from json import JSONDecodeError

def json_deserialize(request_string):

    try:
        result = json.loads(request_string)
        result["ok"] = True
        return result
        
    except JSONDecodeError as error:
        return {
            "ok": False,
            "error": str(error)
        }