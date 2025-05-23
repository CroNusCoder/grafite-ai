try:
    from groq_llama import get_llama_response
    response = get_llama_response("Explain Newton's second law")
    print(response)
except Exception as e:
    print("Error occurred:", e)
