# chroma-server/main.py

from fastapi import FastAPI
import chromadb
import os

# ساخت کلاینت ChromaDB
persist_dir = os.getenv("CHROMA_PERSIST_DIR", ".chroma")
client = chromadb.Client(chromadb.config.Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir))

# تعریف اپلیکیشن FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Chroma is running!"}

@app.get("/collections")
def list_collections():
    collections = client.list_collections()
    return {"collections": [c.name for c in collections]}

@app.post("/collections/{name}")
def create_collection(name: str):
    collection = client.create_collection(name=name)
    return {"message": f"Collection '{name}' created."}

@app.get("/collections/{name}")
def get_collection(name: str):
    collection = client.get_collection(name=name)
    return {"name": collection.name, "count": collection.count()}

@app.delete("/collections/{name}")
def delete_collection(name: str):
    client.delete_collection(name=name)
    return {"message": f"Collection '{name}' deleted."}
