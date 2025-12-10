import os
from mem0 import Memory

os.environ["OPENAI_API_KEY"] = "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"

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4.1-nano-2025-04-14",
            "temperature": 0.2,
            "max_tokens": 2000,
        }
    }
}


m = Memory.from_config(config)
messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I’m not a big fan of thriller movies but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future."}
]
m.add(messages, user_id="alice", metadata={"category": "movies"})