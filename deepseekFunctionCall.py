# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "assistant", "content": "You are a tutor for dance choreography"},
        {"role": "assistant", "content": "You are a classmate for dance choreography cooperation"},
        {"role": "user", "content": "Could you help me to do dance choreography :contemporary,emotional,Solo"},
    ],
    stream=False
)

print(response.choices[0].message.content)