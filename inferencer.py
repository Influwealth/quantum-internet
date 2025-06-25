import requests

def query(prompt):
    return requests.post("https://api.sambanova.ai/v1/infer", json={
        "prompt": prompt,
        "key": "39f8beea-7890-4985-b768-bce87df7a120"
    }).json().get("response", "Error")