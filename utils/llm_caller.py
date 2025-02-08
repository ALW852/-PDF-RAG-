import openai
import os
def call_openai(prompt, model_name):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    client =openai.Client(
        api_key = api_key,
        base_url = base_url
    )
    response = client.chat.completions.create(
        model = model_name,
        temperature = 0.7,
        messages = [{"role":"user", "content":prompt}]
    )
    return(response.choices[0].message.content)
