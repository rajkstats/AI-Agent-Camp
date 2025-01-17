import requests
import json



def chat_with_ollama_stream(prompt, model="llama3.2", system_prompt=None):
    url = "http://localhost:11434/api/chat"
    
    messages = [{"role": "user", "content": prompt}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": True
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if 'message' in chunk:
                    full_response += chunk['message']['content']
                    print(chunk['message']['content'], end='', flush=True)
        return full_response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    prompt = "Why is the sky blue?"
    result = chat_with_ollama_stream(prompt)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Response: {result['message']['content']}")
