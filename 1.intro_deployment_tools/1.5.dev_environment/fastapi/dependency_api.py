from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
import requests


app = FastAPI(title="Hello API")


class CatFact(BaseModel):
    fact: str
    timestamp: datetime


def get_http_client():
    return requests.Session()

@app.get("/cat_facts")
def get_cat_fact(client:requests.Session = Depends(get_http_client)):
    response = client.get("https://catfact.ninja/fact")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="error fetching api")
    fact = response.json()
    return CatFact(fact=fact["fact"], timestamp=datetime.now())

@app.get("/")
def root():
    return {"status": "OK"}

def main():
    """Main function"""
    import uvicorn

    uvicorn.run("dependency_api:app", reload=True)


if __name__ == "__main__":
    # only run this if the file is executed as a script
    main()
