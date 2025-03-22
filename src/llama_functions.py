from groq import Groq
import os
from utils import load_config

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(script_dir, "config.yaml")
config = load_config(config_dir)

groq_key = config['api_keys']['groq']

client = Groq(api_key=groq_key)
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "make a question to llama "
        },
        {
            "role": "assistant",
            "content": "What are some key differences between artificial intelligence and human intelligence, and how can AI systems like yourself be used to augment human capabilities?"
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
