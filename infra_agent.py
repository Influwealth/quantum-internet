import json
import requests

def local_router(prompt):
    if "status" in prompt:
        return " Mesh node online."
    return None

def samba_infer(prompt):
    return requests.post("https://api.sambanova.ai/v1/infer", json={
        "prompt": prompt,
        "key": "39f8beea-7890-4985-b768-bce87df7a120"
    }).json().get("response", "No response")

while True:
    prompt = input(" > ")
    response = local_router(prompt)
    if not response:
        response = samba_infer(prompt)
    print(f"InfraFlow: {response}")