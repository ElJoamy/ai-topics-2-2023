from fastapi import FastAPI

app = FastAPI(title="Microservice")

@app.get("/")
def root():
    return {"status": "OK"}

