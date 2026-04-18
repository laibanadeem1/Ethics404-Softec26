import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6KthTCqyQ4pln440kE5XYX9LuXUJbH4YXwRbjDrBh5Y_g")

models = genai.list_models()

for m in models:
    print(m.name, m.supported_generation_methods)