import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key (first 10 chars): {api_key[:10]}...")

genai.configure(api_key=api_key)

# Try different model names
models_to_try = ['gemini-pro', 'models/gemini-pro', 'gemini-1.5-flash', 'models/gemini-1.5-flash']

for model_name in models_to_try:
    try:
        print(f"\nTrying model: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello")
        print(f"✅ SUCCESS with {model_name}")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"❌ Failed with {model_name}: {str(e)}")

print("\n--- Available Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"• {m.name}")
except Exception as e:
    print(f"Could not list models: {e}")
