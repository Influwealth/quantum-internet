from fastapi import FastAPI
import uvicorn

# This creates a proper web application server
app = FastAPI(title="InfraFlow Agent Server")

@app.get("/")
def read_root():
    # This is the "status page" that will be shown
    return {"status": "online", "message": "InfraFlow Agent Server is running. Ready for missions."}

# This part allows gunicorn to run the app
# It is not directly called but needed by the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
