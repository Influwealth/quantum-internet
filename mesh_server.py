import os
import autogen
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="InfraFlow Quantum Internet Mesh (AutoGen Edition)")
llm_config = {}

class MissionRequest(BaseModel):
    mission: str

def run_autogen_mission(mission: str):
    if not llm_config:
        print("ERROR: LLM Config is not set. Mission aborted.")
        return

    print(f"--- MISSION ACCEPTED: {mission} ---")

    planner = autogen.AssistantAgent(name="Planner", llm_config=llm_config, system_message="You are a master planner. Create a step-by-step plan. End with TERMINATE.")
    strategist = autogen.AssistantAgent(name="Strategist", llm_config=llm_config, system_message="You are a strategist. Execute the tasks given to you.")
    commander = autogen.UserProxyAgent(name="Commander", human_input_mode="NEVER", code_execution_config=False, is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper())

    groupchat = autogen.GroupChat(agents=[commander, planner, strategist], messages=[], max_round=15)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    commander.initiate_chat(manager, message=mission)
    print("--- MISSION CONCLUDED ---")

@app.on_event("startup")
def startup_event():
    global llm_config
    print("🚀 Starting InfraFlow Server (AutoGen Edition)...")
    try:
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config.")

        llm_config = {"config_list": [{"model": "Meta-Llama-3.3-70B-Instruct", "api_key": api_key, "base_url": base_url}]}
        print("✅ AI Engine is ONLINE and configured.")
    except Exception as e:
        print(f"❌ FATAL STARTUP ERROR: {e}")

@app.get("/")
def root_status():
    return {"status": "online" if llm_config else "offline", "engine": "AutoGen DeepSight Core"}

@app.post("/start-mission")
async def start_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    if not llm_config:
        raise HTTPException(status_code=503, detail="AI Engine is not configured.")

    background_tasks.add_task(run_autogen_mission, request.mission)
    return {"status": "mission_accepted", "details": request.mission}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

