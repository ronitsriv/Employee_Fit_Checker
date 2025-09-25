import google.generativeai as genai

# Configure the Gemini API with your API key
API_KEY = "your-api-key-here"
genai.configure(api_key=API_KEY)

# Use a valid model identifier
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Define the prompt for the AI model
prompt = "Classify the following lead as High, Medium, or Low intent: [Lead details here]"

# Generate content using the model
response = model.generate_content(prompt)

# Extract and print the response
ai_response = response.text.strip()
print(ai_response)
