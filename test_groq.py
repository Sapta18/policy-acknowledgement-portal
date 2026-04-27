from groq import Groq

api_key = "your_real_api_key_here"

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}],
        model="llama-3.1-8b-instant"
    )

    print("SUCCESS:")
    print(response.choices[0].message.content)

except Exception as e:
    print("ERROR:", e)