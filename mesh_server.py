import os
import autogen
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="InfraFlow Quantum Internet Mesh Agent Server")
llm_config = {}

class MissionRequest(BaseModel):
    mission: str

def run_mesh_mission(mission: str):
    if not llm_config:
        print("❌ AI Engine config missing, mission aborted.")
        return
    print(f"🌐 Mission received: {mission}")

    # Define the agent crew
    architect = autogen.AssistantAgent(
        name="The_Architect",
        llm_config=llm_config,
        system_message="You are The Architect, an elite AI agent. Your mission is to write complete, production-ready Python functions ('tools') for other agents to use. You must present only the final, complete code in a single block for review."
    )
    commander = autogen.UserProxyAgent(
        name="MeshCommander",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
        code_execution_config=False,
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
    )

    commander.initiate_chat(architect, message=mission)
    print("✅ Mesh mission completed.")

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
            "config_list": [{"model": "Meta-Llama-3.3-70B-Instruct",
                             "api_key": api_key, "base_url": base_url, "price": [0,0]}],
            "temperature": 0.7, "seed": 42
        }
        print("✅ AI Engine configured and online.")
    except Exception as e:
        print(f"❌ Startup error: {e}")
        llm_config = {}

@app.get("/")
def root_status():
    return {"status": "online" if llm_config else "offline", "engine": "DeepSight Agent Core", "message": "Ready for missions. Send a POST to /start-mission"}

@app.post("/start-mission")
async def start_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    if not llm_config:
        raise HTTPException(status_code=503, detail="AI Engine is not configured or offline.")

    mission_prompt = request.mission
    background_tasks.add_task(run_mesh_mission, mission_prompt)
    return {"status": "mission_accepted", "details": mission_prompt}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
