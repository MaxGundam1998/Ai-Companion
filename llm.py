import requests
import json

URL = "http://localhost:8000/api/chat"

MODEL = "llama3.2:3b"

def chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "options": {
            "num_predict": 100
            }
        }
    
    full_response = ""
    
    try:
        with requests.post(
            URL,
            json=payload,
            stream = True,
            timeout = 120
        ) as response:
            
            response.raise_for_status()
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                try:
                    data = json.loads(line.decode("utf-8"))
                
                except json.JSONDecodeError:
                    continue
                
                chunk = data.get("message", {}).get("content", "")
                
                if chunk:
                    print(chunk, end="", flush=True)
                    full_response += chunk
                    
                if data.get("done", False):
                    break
                
    except requests.exceptions.ChunkedEncodingError:
        print("\n[Warning: response ended prematurely]")
        
    except requests.exceptions.RequestException as e:
        print(f"\n[Connection error: {e}]")
        
    print()
    
    return full_response

def background_chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predit": 40
            }
    }
    
    response = requests.post(URL, json=payload, timeout=300)
    response.raise_for_status()
    
    data = response.json()
    
    return data["message"]["content"].strip()


def extract_memory(user_input):
    memory_prompt = [
        {
            "role": "system",
            "content": """
Decide whether the user's message contains a useful long-term fact worth remembering.

Good memories include:
- preferences
- hobbies
- favorite things
- important ongoing projects
- stable personal preferences

Do NOT save:
- greetings
- temporary feelings
- random one-off comments
- questions
- things that are only relevant for a few minutes

If there is a useful memory, return only one short sentence describing it.
If there is nothing worth remembering, return exactly:
NONE
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    return background_chat(memory_prompt)
    