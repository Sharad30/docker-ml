from fastapi import FastAPI
from .job import Job

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "alive!!!"}
