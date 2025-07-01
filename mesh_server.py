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
        print("AI Engine config missing, mission aborted.")
        return
    print(f"Mission received: {mission}")

    # Define the full agent crew from your plan
    planner = autogen.AssistantAgent(name="MeshPlanner", llm_config=llm_config, system_message="Break missions into numbered tasks. End with TERMINATE.")
    strategist = autogen.AssistantAgent(name="MeshStrategist", llm_config=llm_config, system_message="Execute technical and strategic tasks.")
    commander = autogen.UserProxyAgent(name="MeshCommander", human_input_mode="NEVER", code_execution_config=False)

    # In a real app, you would define all 15 agents here.
    # For now, we use a smaller core team for stability.
    groupchat = autogen.GroupChat(
        agents=[commander, planner, strategist],
        messages=[],
        max_round=15
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    commander.initiate_chat(manager, message=mission)
    print("Mesh mission completed.")

@app.on_event("startup")
def startup_event():
    global llm_config
    print("Starting InfraFlow Quantum Mesh Server...")
    try:
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config in environment variables.")
        llm_config = {
            "config_list": [{"model": "Meta-Llama-3.3-70B-Instruct", "api_key": api_key, "base_url": base_url}]
        }
        print("AI Engine configured and online.")
    except Exception as e:
        print(f"Startup error: {e}")

@app.get("/")
def root_status():
    return {"status": "online" if llm_config else "offline", "engine": "InfraFlow Quantum Mesh Agent"}

@app.post("/start-mesh-mission")
async def start_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    if not llm_config:
        raise HTTPException(status_code=503, detail="AI Engine not configured.")
    background_tasks.add_task(run_mesh_mission, request.mission)
    return {"status": "mission_accepted", "details": request.mission}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

