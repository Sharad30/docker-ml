from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .job import Job
from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///database.sqlite")
SQLModel.metadata.create_all(engine)

app = FastAPI()
origins = ["http://localhost:3000", "localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "alive!!!"}


@app.get("/create/job")
def create_job(
    dataset_id: str,
    container_id: str,
    codebase_id: str,
):
    job = Job(
        dataset_id=dataset_id,
        container_id=container_id,
        codebase_id=codebase_id,
        status="pending",
    )
    job.enqueue(engine=engine)
    # TODO: error handling
    # TODO: fetch the id of the created job and return it
    return {"message": "success"}


@app.get("/update/job")
def update_job(job_id: int, new_status: str):
    job = Job(job_id=job_id)
    job.update_status(engine=engine, new_status=new_status)
    # TODO: error handling
    return {"message": "success"}


@app.get("/delete/job")
def delete_job(job_id: int):
    job = Job(job_id=job_id)
    job.dequeue(engine=engine)
    # TODO: error handling
    return {"message": "success"}


@app.get("/list/job")
def list_job(job_id: int):
    job = Job(job_id=job_id)
    status = job.get_status(engine=engine)
    # TODO: error handling
    return {"message": "success", "status": status}


@app.get("/list/jobs")
def list_jobs():
    return {"message": "success"}


@app.get("/request/job")
def request_job():
    return {"message": "success"}


todos = [
    {"id": "1", "item": "Read a book."},
    {"id": "2", "item": "Cycle around town."},
]


@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return {"data": todos}
