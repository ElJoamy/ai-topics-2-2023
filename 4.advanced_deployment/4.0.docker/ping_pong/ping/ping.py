from fastapi import FastAPI
import requests

app = FastAPI(title="PING")

@app.get("/")
def root(message: str):
    response = requests.get(f"http://pong-backend?message={message}")
    if response.status_code == 200:
        return {"status": response.json()}
    return {"status": "error"}
