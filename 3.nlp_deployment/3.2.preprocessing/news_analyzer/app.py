from fastapi import FastAPI, Body, HTTPException, Depends
import time
import requests
from functools import cache
from bs4 import BeautifulSoup
import spacy
from pydantic import BaseModel
import httpx

class ArticleAnalysis(BaseModel):
    url: str            # url del articulo
    length: int         # longitud en caracteres
    title: str          # titulo del articulo
    n_locations: int    # cantidad de ubicaciones unicas mencionadas
    top_location: str
    n_people: int       # cantidad de personas unicas mencionadas
    top_person: str
    n_org: int
    top_org: str

# extra:
# recibir una lista de enlaces:
# devolver una lista ArticleAnalysis

app = FastAPI(title="News Analyzer")

@cache
def get_nlp() -> spacy.language.Language:
    return spacy.load("es_core_news_md")

def get_http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

@app.post("/news")
async def analyze_news(
    url: str = Body(...), 
    nlp=Depends(get_nlp),
    client:httpx.AsyncClient=Depends(get_http_client)
    ):
    # un enlace a un articulo
    # descargar el texto
    start_time = time.time()
    # response = requests.get(url)
    req = client.build_request("GET", url)
    response = await client.send(req)
    response_time = time.time() - start_time
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="request failed!")
    # extraer el texto del articulo
    html = response.text
    start_time = time.time()
    soup = BeautifulSoup(html, "html.parser")
    text_elements = soup.find_all("div", class_="text-editor")
    texts = [elem.get_text() for elem in text_elements]
    extract_time = time.time() - start_time
    # procesar el texto
    start_time = time.time()
    doc = nlp(texts[0])
    process_time = time.time() - start_time
    # almacenar resultados
    # retornar resultados
    return {
        "response_ms": response_time * 1000, 
        "extract_ms": extract_time * 1000,
        "process_ms": process_time * 100, 
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)