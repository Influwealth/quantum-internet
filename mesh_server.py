from fastapi import FastAPI
import uvicorn

# This creates a proper web application server
app = FastAPI(title="InfraFlow Agent Server")

@app.get("/")
def read_root():
    # This is the "status page" that will be shown
    return {"status": "online", "message": "InfraFlow Agent Server is running. Ready for missions."}

@app.post("/start-mesh-mission")
def start_mission():
    # This is a placeholder to confirm the endpoint works.
    # We will add the real agent logic back in the next step.
    print("--- MISSION COMMAND RECEIVED ---")
    return {"status": "mission_accepted", "details": "The mission command was received successfully."}

# This part allows gunicorn to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

