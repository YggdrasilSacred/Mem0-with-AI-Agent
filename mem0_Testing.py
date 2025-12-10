from mem0 import Memory
from ollama import ChatResponse
from ollama import chat
from supabase import create_client, Client
import os


config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "gemma3:1b",
            "temperature": 1,
            "max_tokens": 2000,
        }
    },

    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1"
        }
    },

    # "vector_store": {
    #     "provider": "qdrant",
    #     "config": {
    #         "collection_name": "test",  
    #         "embedding_model_dims":384, # hard coded to match the embedding dim of the model
    #     }
    # },

    "vector_store": {
        "provider": "supabase",
        "config": {
            "connection_string": 'postgresql://postgres.oztnarmlcistwjyslwns:Sacredyggdrasil69?@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres',
            "collection_name": "memories",
            "embedding_model_dims": 384
        }
    }
}



memory = Memory.from_config(config)

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)  # Limits how many columns of data to recall per message
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    
    # Generate Assistant response
    system_prompt = f"You are a helpful AI. Answer the question in a user friendly way based on query and memories.\nUser Memories:\n{memories_str}"   
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response : ChatResponse = chat(model="gemma3:1b", messages=messages)
    assistant_response = response.message.content

    # Create new memories from the conversation
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages[1], user_id=user_id, infer=False)  # Force extract the message with "user" role
    print("\nMessages: " + str(messages) + "\n")

    return assistant_response



# def delete_oldest():
#     url: str = os.environ.get("postgresql://postgres.oztnarmlcistwjyslwns:Sacredyggdrasil69?@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres")
#     key: str = os.environ.get("sb_publishable_Zl5L3QOK8jXmU1TXalS6ig_-4qNViZX")
#     supabase: Client = create_client(url, key)

#     response = supabase.table("memories").select("metadata").execute()
#     data = response.data 
#     print("Data from supabase: " + str(data))



def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            # delete_oldest()
            break
        print(f"AI: {chat_with_memories(user_input)}")


if __name__ == "__main__":
    main()