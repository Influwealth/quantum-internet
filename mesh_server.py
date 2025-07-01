import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

app = FastAPI(title="InfraFlow Quantum Internet Mesh (CrewAI Edition)")
llm_config = None

class MissionRequest(BaseModel):
    mission: str

def run_crew_mission(mission: str):
    if not llm_config:
        print("ERROR: LLM is not configured. Mission aborted.")
        return

    print(f"--- MISSION ACCEPTED: {mission} ---")

    # Define the CrewAI agents
    planner = Agent(
        role="Master Planner",
        goal="Create a clear, step-by-step plan from high-level missions.",
        backstory="A strategic thinker known for exceptional planning.",
        llm=llm_config,
        verbose=True
    )
    strategist = Agent(
        role="Mesh Strategist",
        goal="Execute technical and strategic tasks as assigned.",
        backstory="An expert in deploying decentralized network strategies.",
        llm=llm_config,
        verbose=True
    )

    # Define the tasks for the crew
    planning_task = Task(
        description=mission,
        expected_output="A detailed, numbered list of tasks for the strategist to execute.",
        agent=planner
    )
    execution_task = Task(
        description="Execute the step-by-step plan provided by the MeshPlanner.",
        expected_output="A summary of the actions taken and the final result.",
        agent=strategist,
        context=[planning_task]
    )

    # Assemble and launch the crew
    mission_crew = Crew(
        agents=[planner, strategist],
        tasks=[planning_task, execution_task],
        verbose=2
    )

    result = mission_crew.kickoff()
    print("--- MISSION CONCLUDED ---")
    print("Final Result:", result)

@app.on_event("startup")
def startup_event():
    global llm_config
    print("🚀 Starting InfraFlow Server (CrewAI Edition)...")
    try:
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config in environment variables.")

        # Configure the LLM for CrewAI via LangChain
        llm_config = ChatOpenAI(
            model="Meta-Llama-3.3-70B-Instruct",
            base_url=base_url,
            api_key=api_key,
        )
        print("✅ AI Engine (CrewAI) is ONLINE and configured.")
    except Exception as e:
        print(f"❌ FATAL STARTUP ERROR: {e}")

@app.get("/")
def root_status():
    return {"status": "online" if llm_config else "offline", "engine": "CrewAI DeepSight Core"}

@app.post("/start-mission")
async def start_mission(request: MissionRequest, background_tasks: BackgroundTasks):
    if not llm_config:
        raise HTTPException(status_code=503, detail="AI Engine is not configured or offline.")

    background_tasks.add_task(run_crew_mission, request.mission)
    return {"status": "mission_accepted", "details": f"Crew dispatched with mission: {request.mission}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

