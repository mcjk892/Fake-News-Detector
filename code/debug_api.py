import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from groq import Groq
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROK_API_KEY")
if api_key:
    api_key = api_key.strip("'\"")

print(f"API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'NONE'}")

# 1. Test Search
print("\n--- Testing DuckDuckGo Search ---")
try:
    with DDGS() as ddgs:
        results = ddgs.text("Is world flat?", max_results=3, backend='html')
        for r in results:
            print(f"Found: {r['href']}")
except Exception as e:
    print(f"Search Error: {e}")

# 2. Test AI
print("\n--- Testing Groq AI ---")
if not api_key:
    print("No API Key found in .env!")
else:
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": "Hello, this is a test fact-check request."}
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            reasoning_effort="medium",
            stream=False
        )
        print(f"AI Response: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"AI Error: {e}")
        if "getaddrinfo failed" in str(e):
            print("\n!!! TROUBLESHOOTING: NameResolutionError detected !!!")
            print("1. Check if your computer has internet access.")
            print("2. Try disabling any VPN or Firewall.")
            print("3. Try changing your DNS to Google (8.8.8.8) or Cloudflare (1.1.1.1).")
