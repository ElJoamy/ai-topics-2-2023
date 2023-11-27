from fastapi import FastAPI, Depends
from llm_service import TemplateLLM
from prompts import ProjectParams
from parsers import ProjectIdeas
from config import get_settings

_SETTINGS = get_settings()


app = FastAPI(title=_SETTINGS.service_name)


def get_llm_service():
    return TemplateLLM()

@app.post("/generate")
def generate_ideas(
    params: ProjectParams,
    service: TemplateLLM = Depends(get_llm_service),
) -> ProjectIdeas:
    return service.generate(params)


@app.get("/")
def root():
    return {"status": "OK"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)