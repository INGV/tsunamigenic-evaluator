import json
from datetime import datetime

def completeErrorStruct(req, data):
    data["instance"] = req.url
    data["type"] = ""
    data["request_submitted"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S UTC')
    data["version"] = "1.0"
    return json.dumps(data)