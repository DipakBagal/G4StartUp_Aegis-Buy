import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Testing API Key: {api_key[:20]}...\n")

# List available models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get('models', [])
    print(f"✅ Found {len(models)} models:\n")
    
    for model in models:
        name = model.get('name', '').replace('models/', '')
        methods = model.get('supportedGenerationMethods', [])
        
        if 'generateContent' in methods:
            print(f"✓ {name}")
            print(f"  Methods: {', '.join(methods)}")
            print()
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())
