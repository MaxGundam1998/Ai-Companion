import requests

URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


def extract_memory(user_input):
    prompt = f"""
Extract a personal fact from the user's message.

Save stable personal facts, preferences, possessions, relationships,
recurring habits, skills, long-term goals, and ongoing projects.

Return NONE for temporary states, one-time events, current activities,
short-term plans, questions, and temporary problems.

A fact does not need to be permanent. Save it if it describes the user's
general life, preferences, identity, routine, interests, or ongoing goals
rather than what is happening at one particular moment.

Do NOT create a memory just because a message contains information about the user.

Temporary states, one-time events, current activities, recent events, vague
opinions, and information inferred from a question are NOT memories.

Examples of temporary information that must return NONE:
- being hungry, tired, sad, excited, or busy right now
- what the user ate today
- what the user is doing right now
- something that happened once
- a temporary technical problem
- winning or losing a game or match
- plans for later today

Follow these examples exactly.

User: Hello, Nikki!
Memory: NONE

User: How are you today?
Memory: NONE

User: What's the capital of Japan?
Memory: NONE

User: My name is Michael.
Memory: The user's name is Michael.

User: My favorite color is green.
Memory: The user's favorite color is green.

User: I like playing video games.
Memory: The user likes playing video games.

User: I enjoy building model kits.
Memory: The user enjoys building model kits.

User: Fire Emblem is one of my favorite game series.
Memory: Fire Emblem is one of the user's favorite game series.

Return only the memory sentence or NONE.
Do not explain your answer.

User message:
{user_input}

Memory:
"""
    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 50
            }
        },
        timeout=60
    )
    
    response.raise_for_status()
    
    data = response.json()
    
    memory_text = data["response"].strip()
    
    if memory_text.lower().startswith("memory:"):
        memory_text = memory_text[7:].strip()
    
    return memory_text

