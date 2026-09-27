import requests
import json
import re
import time

URL = "http://localhost:8000/api/chat"

MODEL = "llama3.2:3b"

def do_chat_request(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "options": {
            "num_predict": 200,
            "temperature": 0.6,
            "top_p": 0.85,
            "stop": ["<|eot_id|>", "<|start_header_id|>"]
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
                    #print("\n\nDEBUG DONE:", data)
                    break
                
    except requests.exceptions.ChunkedEncodingError as e:
        print("\n[Warning: response ended prematurely]")
        print("Streaming error:", repr(e))
        
    except requests.exceptions.RequestException as e:
        print(f"\n[Connection error: {e}]")
        
    
    return full_response

def clean_response(text):
    for marker in ["<|eot_id|>", "<|start_header_id|>"]:
        if marker in text:
            text = text.split(marker)[0]
            
    text = re.split(r"\n\(I ", text)[0]
    
    return text.strip()

def chat(messages, retries=1):
    for attempt in range(retries + 1):
        raw_response = do_chat_request(messages)
        cleaned = clean_response(raw_response)
        
        if cleaned:
            return cleaned
        
        if attempt < retries:
            print("\n[Retrying...]")
            time.sleep(1)
            
            
    return cleaned