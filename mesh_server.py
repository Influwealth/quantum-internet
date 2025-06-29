import os
import autogen
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- App Initialization ---
app = FastAPI(title="InfraFlow Quantum Internet Mesh Agent Server")
llm_config = {}

# This defines the structure of the incoming mission requests
class MissionRequest(BaseModel):
    mission: str

def run_mesh_mission(mission: str):
    """
    This function assembles and runs the agent crew for a given mission.
    """
    try:
        if not llm_config:
            logger.error("LLM Configuration is not set. Mission aborted.")
            return

        logger.info(f"--- MISSION ACCEPTED: {mission} ---")

        # Define the agents based on your DeepSight plan
        planner = autogen.AssistantAgent(
            name="MeshPlanner",
            llm_config=llm_config,
            system_message="You are a master planner. You create clear, step-by-step plans from high-level missions. You do not execute the plan yourself. End your plan with TERMINATE."
        )
        strategist = autogen.AssistantAgent(
            name="MeshStrategist",
            llm_config=llm_config,
            system_message="You are a Mesh Strategist. You execute technical and strategic tasks assigned by the Commander."
        )
        commander = autogen.UserProxyAgent(
            name="MeshCommander",
            human_input_mode="NEVER",
            max_consecutive_auto_reply= 20,
            code_execution_config=False,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
        )

        # Set up the collaborative group chat
        groupchat = autogen.GroupChat(
            agents=[commander, planner, strategist], # Add more agents as needed
            messages=[],
            max_round= 25
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # The Commander kicks off the mission with the dynamic prompt
        commander.initiate_chat(manager, message=mission)

        logger.info(f"--- MISSION CONCLUDED ---")
    except Exception as e:
        logger.error(f"Error running mission: {e}")

@app.on_event("startup")
def startup_event():
    """
    This runs once when the Render server starts to configure the AI Engine.
    """
    global llm_config
    logger.info("Starting InfraFlow Server...")
    try:
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config in environment variables.")

        llm_config = {
            "config_list": [{"model": "Meta-Llama-3.3-70B-Instruct", "api_key": api_key, "base_url": base_url, "price": [0,0]}],
            "temperature": 0.7, "seed": 42
        }
        logger.info("AI Engine is ONLINE and configured.")
    except Exception as e:
        logger.error(f"FATAL STARTUP ERROR: {e}")

@app.get("/")
def root_status():
    """ A simple status check endpoint. """
    return {"status": "online" if llm_config else "offline", "engine": "InfraFlow Quantum Mesh Agent"}

@app.post("/start-mesh-mission")
async def start_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    """
    This is the REAL mission endpoint. It receives your command and gives it to the agents.
    """
    if not llm_config:
        raise HTTPException(status_code= 503, detail="AI Engine is not configured or offline.")
    
    # Take the mission from the request and send it to the agents
    mission_prompt = request.mission
    background_tasks.add_task(run_mesh_mission, mission_prompt)
    
    return {"status": "mission_accepted", "details": f"The DeepSight crew has been tasked with: {mission_prompt}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port= 8000)
