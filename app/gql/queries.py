from graphene import ObjectType, List, Int, Field
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject
from app.db.database import Session
from app.db.models import Job, Employer, User, JobApplication
from app.utils import admin_user


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id = Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id = Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_job(root, info, id):
        with Session() as session:
            job = (
                session.query(Job)
                .filter(Job.id==id)
                .first()
            )
        return job

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            jobs = (
                session.query(Job)
                .all()
            )
        return jobs


    @staticmethod
    def resolve_employer(root, info, id):
        with Session() as session:
            employers = (
                session.query(Employer)
                .filter(Employer.id==id)
                .first()
            )
        return employers

    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            employers = session.query(Employer).all()
        return employers
    
    @staticmethod
    def resolve_users(root, info):
        with Session() as session:
            users = session.query(User).all()
        return users

    @admin_user
    def resolve_job_applications(root, info):
        with Session() as session:
            applications = (
                session.query(JobApplication)
                .all()
            )
        return applications
