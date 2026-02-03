import ollama

# We'll use 'tinyllama', which is the standard 1.1b version 
# Ollama handles the quantization automatically (usually 4-bit)
model_name = "tinyllama"

prompt = "What is the reason of life? Respond in one word only."

# Generate the response
response = ollama.generate(model=model_name, prompt=prompt)

# The response is a dictionary; we grab the 'response' key
answer = response['response'].strip()

print(f"The answer is: {answer}")