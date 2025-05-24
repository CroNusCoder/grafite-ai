from groq_llama import get_llama_response

query = "A ball is thrown vertically upward with a speed of 20 m/s. How high will it go?"
system_prompt = "You're a JEE/NEET physics tutor. Explain step-by-step how to approach the question."

response = get_llama_response(prompt=query, system_prompt=system_prompt)
print(response)

