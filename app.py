from llm import chat
from character import CHARACTER
from memory_manager import extract_memory
from tts import speak
import memory

NIKKI_BANNER = r"""
 ███╗   ██╗██╗██╗  ██╗██╗  ██╗██╗
 ████╗  ██║██║██║ ██╔╝██║ ██╔╝██║
 ██╔██╗ ██║██║█████╔╝ █████╔╝ ██║
 ██║╚██╗██║██║██╔═██╗ ██╔═██╗ ██║
 ██║ ╚████║██║██║  ██╗██║  ██╗██║
 ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
"""

#Initialize memory
memory.initialize()

print(NIKKI_BANNER)
print("Warming up model...")
chat([{"role": "user", "content": "Hi"}])
print("Nikki online.")
print("Use 'goodbye' to exit")
print()


while True:
    #Start of input
    user_input = input("\nYou: ")
    
    #Exit prompt
    if user_input.lower() == "goodbye":
        break
    
    if not user_input:
        continue
    
        
    #Recent Conversation History
    history = memory.recent_message(2)
    
    #Find relevant long-term memories
    memories = memory.search_memories(user_input, 5)
    
    memory_text = "\n".join(memories)
    
    
    system_prompt = f"""
    {CHARACTER}
    
    KNOWN FACTS ABOUT THE USER:
    {memory_text}
    
    The facts above describe the USER, not Nikki.
    Use them only when they are relevant to the user's current message.
    Do not mention the memory system or explain that you remembered something.
    
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
        #Generate Nikki's response
        print("\nNikki: ", end="", flush=True)
        response = chat(messages).strip()
        print()
        
        memory.save_message("user", user_input)
        memory.save_message("assistant", response)
        
        speak(response)
        
        #Memory extraction
        try:
            new_memory = extract_memory(user_input)
            if new_memory.strip().upper() != "NONE":
                memory.save_memory(new_memory)
                
        except Exception as e:
            print(f"[memory skipped: {e}]")
            
        
    except Exception as e:
        print("\nNikki had trouble responding.")
        print("Error:", e)


