import requests

def get_ollama_response(message, temperature=0.7, max_length=500, top_p=0.9):
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "llama3.2",
                                   "prompt": message,
                                   "stream": False,
                                   "temperature": temperature,
                                   "max_length": max_length,
                                   "top_p": top_p
                               })
        return response.json()['response']
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"