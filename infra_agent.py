import json, requests, os
from datetime import datetime

CONFIG_FILE = "agent_config.json"
LOG_FILE = "mesh_local.log"

def load_config():
    with open(CONFIG_FILE) as f: return json.load(f)

def log_event(event):
    with open(LOG_FILE, "a") as f: f.write(f"{datetime.now().isoformat()} | {event}\n")

def send_prompt(prompt):
    config = load_config()
    try:
        r = requests.post("http://localhost:8000/start-mesh-mission", timeout=10)
        print("Server response:", r.json())
        log_event(f"Prompt: {prompt} | Status: {r.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}"); log_event(f"Error: {e}")

if __name__ == "__main__":
    print("🤖 InfraFlow Local CLI Agent"); p = input("Enter prompt: "); send_prompt(p)


