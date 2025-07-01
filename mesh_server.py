import os
import autogen
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn

# --- App Initialization ---
app = FastAPI(title="InfraFlow DeepSight Agent Server")

# --- Global Configuration ---
llm_config = {}

# --- Define the structure for incoming missions ---
class MissionRequest(BaseModel):
    mission: str

# --- This is the function that runs your agent crew ---
def run_autogen_mission(mission: str):
    if not llm_config:
        print("ERROR: LLM Config is not set. Mission aborted.")
        return

    print(f"--- MISSION ACCEPTED: {mission} ---")
    
    # Define the agents from your DeepSight plan
    planner = autogen.AssistantAgent(
        name="Planner",
        llm_config=llm_config,
        system_message="You are a master planner. You create clear, step-by-step plans from high-level missions. You do not execute the plan yourself. End your plan with the word TERMINATE."
    )
    strategist = autogen.AssistantAgent(
        name="Strategist",
        llm_config=llm_config,
        system_message="You are a strategist. You execute the technical and strategic tasks assigned to you by the Commander."
    )
    commander = autogen.UserProxyAgent(
        name="Commander",
        human_input_mode="NEVER",
        code_execution_config=False,
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
    )
    
    # Set up the collaborative group chat
    groupchat = autogen.GroupChat(
        agents=[commander, planner, strategist],
        messages=[],
        max_round=15
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    # The Commander kicks off the mission
    commander.initiate_chat(manager, message=mission)
    print("--- MISSION CONCLUDED ---")

# --- This runs once when the Render server starts ---
@app.on_event("startup")
def startup_event():
    global llm_config
    print("🚀 Starting InfraFlow Server (AutoGen Edition)...")
    try:
        # These are read from Render's Environment Variables
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config.")
        
        # THIS IS THE UPGRADED MODEL
        llm_config = {
            "config_list": [{"model": "Llama-4-Maverick-17B-128E-Instruct", "api_key": api_key, "base_url": base_url}]
        }
        print("✅ AI Engine is ONLINE and configured with Llama 4.")
    except Exception as e:
        print(f"❌ FATAL STARTUP ERROR: {e}")

# --- API Endpoints ---
@app.get("/")
def root_status():
    return {"status": "online" if llm_config else "offline", "engine": "AutoGen DeepSight Core"}

@app.post("/start-mission")
async def start_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    if not llm_config:
        raise HTTPException(status_code=503, detail="AI Engine is not configured.")
    
    background_tasks.add_task(run_autogen_mission, request.mission)
    return {"status": "mission_accepted", "details": request.mission}





