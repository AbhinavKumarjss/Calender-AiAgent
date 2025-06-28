import json, re

def extract_json(response: str):
    try:
        print("Original response:", response)
        # Remove markdown code blocks
        match = response[response.find('```json')+7:-4];
        match = re.sub(r'```\s*$', '', match)
        print("Cleaned response:", match)
        if match:
            return json.loads(match)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    return {"error": "Invalid JSON"}