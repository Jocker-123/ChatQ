from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from rag.ingest import ingest_to_vector_db, load_docs, search_faiss
from rag.search import search_elasticsearch, index_to_elasticsearch
from rag.websearch import web_search
from rag.llm_pipeline import run_rag_pipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"data/raw_docs/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        docs = load_docs(file_path)
        index_to_elasticsearch(docs)
        msg = ingest_to_vector_db(file_path)
    except Exception as e:
        print(e)
        return {f"status": {e}}
    return RedirectResponse("/", status_code=302)

@app.get("/query_ui", response_class=HTMLResponse)
async def query_ui(request: Request, query: str):
    response = "Unable to access LLM service"

    try:
        vector_results = search_faiss(query)
        elastic_results = search_elasticsearch(query)
        web_results = web_search(query)
        response = run_rag_pipeline(query, vector_results, elastic_results, web_results)
    except Exception as e:
        print(e)
    return templates.TemplateResponse("index.html", {"request": request, "response": response})
