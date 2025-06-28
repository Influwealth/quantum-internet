import os
import autogen
from fastapi import FastAPI, BackgroundTasks, HTTPException
import uvicorn

app = FastAPI(title="InfraFlow Quantum Internet Mesh Agent Server")
llm_config = {}

def run_mesh_mission(mission: str):
    if not llm_config:
        print("❌ AI Engine config missing, mission aborted.")
        return
    print(f"🌐 Mission received: {mission}")

    infra_agent = autogen.AssistantAgent(
        name="InfraAgent",
        llm_config=llm_config,
        system_message="Central router and reasoning engine; delegates to specialized agents."
    )
    planner = autogen.AssistantAgent(
        name="MeshPlanner",
        llm_config=llm_config,
        system_message="Break big missions into numbered tasks. End with TERMINATE."
    )
    strategist = autogen.AssistantAgent(
        name="MeshStrategist",
        llm_config=llm_config,
        system_message="Execute tasks: deploy mesh, quantum routing, AI orchestration."
    )
    compliance = autogen.AssistantAgent(
        name="ComplianceAgent",
        llm_config=llm_config,
        system_message="Ensure compliance with data, AI, quantum encryption laws."
    )
    finance = autogen.AssistantAgent(
        name="FinanceAgent",
        llm_config=llm_config,
        system_message="Create monetization, pricing, subsidy strategies."
    )
    company_formation = autogen.AssistantAgent(
        name="CompanyFormationAgent",
        llm_config=llm_config,
        system_message="Plan LLC, EIN, grants, legal filings."
    )
    quantum_security = autogen.AssistantAgent(
        name="QuantumAISecurity",
        llm_config=llm_config,
        system_message="Design quantum encryption, QKD, threat detection."
    )
    qiaa = autogen.AssistantAgent(
        name="QIAA",
        llm_config=llm_config,
        system_message="Customer interface: provision plans, billing, quantum-to-classical translation."
    )
    revenue_agent = autogen.AssistantAgent(
        name="RevenueAgent",
        llm_config=llm_config,
        system_message="Forecast revenue, optimize plans, model ROI."
    )
    commander = autogen.UserProxyAgent(
        name="MeshCommander",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=20,
        code_execution_config=False,
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
    )

    groupchat = autogen.GroupChat(
        agents=[commander, infra_agent, planner, strategist, compliance,
                finance, company_formation, quantum_security, qiaa, revenue_agent],
        messages=[],
        max_round=25
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    commander.initiate_chat(manager, message=mission)
    print("✅ Mesh mission completed.")

@app.on_event("startup")
def startup_event():
    global llm_config
    print("🚀 Starting InfraFlow Quantum Mesh Server...")
    try:
        api_key = os.environ.get("SAMBANOVA_API_KEY")
        base_url = os.environ.get("SAMBANOVA_BASE_URL")
        if not api_key or not base_url:
            raise ValueError("Missing SambaNova API config in environment variables.")
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
    return {"status": "online" if llm_config else "offline",
            "engine": "InfraFlow Quantum Mesh Agent",
            "message": "POST to /start-mesh-mission" if llm_config else "Check server logs for startup errors."}

@app.post("/start-mesh-mission")
async def start_mesh_mission(background_tasks: BackgroundTasks):
    if not llm_config:
        raise HTTPException(status_code=503, detail="AI Engine not configured or offline.")
    mission = (
        "MeshPlanner, create detailed plan for Quantum Internet beta. "
        "QIAA provisions users; FinanceAgent models revenue; ComplianceAgent checks laws; "
        "QuantumAISecurity ensures encryption; MeshStrategist executes step 1. TERMINATE."
    )
    background_tasks.add_task(run_mesh_mission, mission)
    return {"status": "mission_started", "mission": mission}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
