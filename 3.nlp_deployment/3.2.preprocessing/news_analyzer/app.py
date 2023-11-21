from fastapi import FastAPI, Body, HTTPException, Depends
import requests
from functools import cache
from bs4 import BeautifulSoup
import spacy
from pydantic import BaseModel

class ArticleAnalysis(BaseModel):
    url: str    # url del articulo
    length: int # longitud en caracteres
    title: str  # titulo del articulo
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
def get_nlp():
    return spacy.load("es_core_news_md")

@app.post("/news")
def analyze_news(url: str = Body(...), nlp=Depends(get_nlp)):
    # un enlace a un articulo
    # descargar el texto
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="request failed!")
    # extraer el texto del articulo
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    text_elements = soup.find_all("div", class_="text-editor")
    texts = [elem.get_text() for elem in text_elements]
    # procesar el texto
    doc = nlp(texts[0])
    # almacenar resultados
    # retornar resultados
    return {}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)