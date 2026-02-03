import json
import urllib.request

BASE_URL = "https://integrator.app.thecoderegistry.com/api/ai/router"
API_KEY = "your-api-key"

payload = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "list_projects",
        "arguments": {},
    },
    "id": 1,
}

req = urllib.request.Request(
    BASE_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
    },
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    body = json.loads(resp.read().decode("utf-8"))
    result_text = body["result"]["content"][0]["text"]
    print(json.loads(result_text))
