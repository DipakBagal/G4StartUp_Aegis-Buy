import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing API Key: {api_key[:20]}...")

# Configure
genai.configure(api_key=api_key)

# Try to list available models
print("\n🔍 Checking available models...")
try:
    models = genai.list_models()
    print("\n✅ Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
    # Try to generate content
    print("\n🧪 Testing content generation...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'API key is working!'")
    print(f"\n✅ SUCCESS: {response.text}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 Solution: Enable Gemini API for your project at:")
    print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
