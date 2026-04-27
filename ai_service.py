from groq import Groq
import time

client = Groq(api_key="your_real_api_key_here")

def get_ai_response(user_input):
    retries = 3
    delay = 2  # seconds

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Always give clear, simple, and well-structured answers. Use easy language, bullet points if needed, and avoid confusion."},
                    {"role": "user", "content": user_input}
                    ],
                model="llama-3.1-8b-instant"
                )

            # JSON parsing
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error occurred: {e}")

            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # backoff (2 → 4 → 8)
            else:
                return "Error: Unable to get response from AI"