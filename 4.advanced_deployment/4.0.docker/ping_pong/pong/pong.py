from fastapi import FastAPI

app = FastAPI(title="PONG")

@app.get("/")
def root(message: str):
    if message.lower() == "ping":
        return {"status": "PONG"}
    return {"status": "NO OK"}

