from graphene import Mutation, String, Int, Field, Boolean
from app.gql.types import JobObject
from app.db.database import Session
from app.db.models import Job
from sqlalchemy.orm import joinedload

class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        with Session() as session:
            job = Job(title=title, description=description, employer_id=employer_id)
            session.add(job)
            session.commit()
            session.refresh(job)
        return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(JobObject)

    @staticmethod
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        with Session() as session:
            job = session.query(Job).filter(Job.id==job_id).options(joinedload(Job.employer)).first()

            if not job:
                raise Exception("Job not found")

            if title:
                job.title = title
            if description:
                job.description = description
            if employer_id:
                job.employer_id = employer_id

            session.commit()
            session.refresh(job)
        return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            job = session.query(Job).filter(Job.id==id).first()

            if not job:
                raise Exception("Job not found")
            
            session.delete(job)
            session.commit()
            return DeleteJob(success=True)
