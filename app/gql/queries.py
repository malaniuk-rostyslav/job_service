from graphene import ObjectType, List, Int, Field
from app.gql.types import JobObject, EmployerObject
from app.db.database import Session
from app.db.models import Job, Employer
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id = Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id = Int(required=True))

    @staticmethod
    def resolve_job(root, info, id):
        with Session() as session:
            job = session.query(Job).filter(Job.id==id).options(joinedload(Job.employer)).first()
        return job

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            jobs = session.query(Job).options(joinedload(Job.employer)).all()
        return jobs


    @staticmethod
    def resolve_employer(root, info, id):
        with Session() as session:
            employers = session.query(Employer).filter(Employer.id==id).options(joinedload(Employer.jobs)).first()
        return employers

    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            employers = session.query(Employer).options(joinedload(Employer.jobs)).all()
        return employers
