
import requests
from openai import OpenAI
def call_ai(messages: str)-> str:
    r = requests.get("http://localhost:8000/api/v1/models")

    # Initialize the client to use Lemonade Server
    client = OpenAI(
        base_url="http://localhost:8000/api/v1",
        api_key="lemonade"  # required but unused
    )

    # Create a chat completion
    completion = client.chat.completions.create(
        model="Qwen2.5-0.5B-Instruct-CPU",  # or any other available model
        messages=[
            {"role": "user", "content": messages}
        ]
    )

    # Print the response
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


#call_ai( "What is the capital of France?")