import os
import autogen
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="InfraFlow Quantum Internet Mesh Agent Server")
llm_config = {}

# This is the mission the agents will run
MISSION = (
    "MeshPlanner, create detailed plan for Quantum Internet beta. "
    "QIAA provisions users; FinanceAgent models revenue; ComplianceAgent checks laws; "
    "QuantumAISecurity ensures encryption; MeshStrategist executes step 1. TERMINATE."
)

@app.on_event("startup")
def startup_event():
    global llm_config
    print("🚀 Starting InfraFlow Quantum Mesh Server...")
    try:
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config.")

        llm_config = {
            "config_list": [{"model": "Meta-Llama-3.3-70B-Instruct", "api_key": api_key, "base_url": base_url}],
            "temperature": 0.7
        }
        print("✅ AI Engine configured and online.")
    except Exception as e:
        print(f"❌ Startup error: {e}")

@app.post("/start-mesh-mission")
def start_mesh_mission():
    if not llm_config:
        return {"status": "error", "detail": "AI Engine not configured or offline."}

    print(f"🌐 Mission received: {MISSION}")

    # Define the agent crew
    planner = autogen.AssistantAgent(name="MeshPlanner", llm_config=llm_config)
    strategist = autogen.AssistantAgent(name="MeshStrategist", llm_config=llm_config)
    commander = autogen.UserProxyAgent(name="MeshCommander", human_input_mode="NEVER", code_execution_config=False)

    # In a real app, you'd have a more complex group chat.
    # For this launch, we simplify to a direct command.
    commander.initiate_chat(planner, message=MISSION)

    return {"status": "mission_completed", "details": "The DeepSight crew has finished its planning phase."}

@app.get("/")
def root_status():
    return {"status": "online", "engine": "InfraFlow Quantum Mesh Agent"}
