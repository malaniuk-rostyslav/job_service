from graphene import ObjectType, List
from app.gql.types import JobObject, EmployerObject
from app.db.database import Session
from app.db.models import Job, Employer
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)


    @staticmethod
    def resolve_jobs(root, info):
        return Session().query(Job).options(joinedload(Job.employer)).all()
    
    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).options(joinedload(Employer.jobs)).all()
