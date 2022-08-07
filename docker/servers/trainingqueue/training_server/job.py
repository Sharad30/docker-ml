from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.future.engine import Engine


class Job(SQLModel, table=True):
    job_id: Optional[int] = Field(default=None, primary_key=True)
    dataset_id: Optional[str]
    container_id: Optional[str]
    codebase_id: Optional[str]
    status: Optional[str]

    def update_status(self, engine: Engine, new_status: str):
        with Session(engine) as session:
            statement = select(Job).where(Job.job_id == self.job_id)
            job = session.exec(statement).first()
            job.status = new_status
            session.add(job)
            session.commit()
            session.refresh(job)
            return job

    def get_status(self, engine: Engine):
        with Session(engine) as session:
            statement = select(Job).where(Job.job_id == self.job_id)
            job = session.exec(statement).first()
            return job.status

    def enqueue(self, engine: Engine):
        with Session(engine) as session:
            session.add(self)
            session.commit()
            # TODO: error handling
            return "success"

    def dequeue(self, engine: Engine):
        with Session(engine) as session:
            session.delete(self)
            session.commit()
            # TODO: error handling
            return "success"
