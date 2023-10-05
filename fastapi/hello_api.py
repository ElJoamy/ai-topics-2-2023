from fastapi import FastAPI
import uvicorn


app = FastAPI(title="Hello API")


@app.get("/")
def root():
    return {"message": "hello", "status": "OK"}


if __name__ == "__main__":
    uvicorn.run("hello_api:app", reload=True)
