from llm import chat, extract_memory
from character import CHARACTER
import memory


memory.initialize()

print("Nikki online.")
print("Use 'goodbye' to exit")
print()

while True:
    
    user_input = input("You: ")
    
    if user_input.lower() == "goodbye":
        break
    
    if not user_input:
        continue
    
    history = memory.recent_message(4)
    memories = memory.get_memories(5)
    
    memory_text = "\n".join(memories)
    
    
    system_prompt = CHARACTER +f"""

    Here are some things you remember about the user:
    
    {memory_text}
    
    Use these memories naturally when they are relevant.
    Do not mention that you are reading from a database.
    """
    
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
        
    ]
    
    messages.extend(history)
    
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    try:
        print("\nNikki: ", end="", flush=True)
        
        response = chat(messages)
        
        print()
    
        memory.save_message("user", user_input)
        memory.save_message("assistant", response)
        
        try:
        
            new_memory = extract_memory(user_input)
        
            if not new_memory.strip().upper().startswith("NONE"):
                memory.save_memory(new_memory)
                
        except Exception as e:
            print("[Memory check failed]")
            print("Memory error:", repr(e))
    
    except Exception as e:
        print("\nNikki had trouble responding.")
        print("Error:", e)
