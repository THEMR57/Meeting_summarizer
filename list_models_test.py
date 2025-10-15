import os
import google.generativeai as genai

# set your key
gemini_key = os.getenv("GEMINI_API_KEY") or "YOUR_KEY_HERE"
genai.configure(api_key=gemini_key)

def show_models():
    models = genai.list_models()
    print("All models:")
    for m in models:
        print(f"- {m.name} supports: {m.supported_generation_methods}")
    # optionally filter those that support generateContent
    print("\nModels supporting generateContent:")
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            print(f"  * {m.name}")

if __name__ == "__main__":
    show_models()
