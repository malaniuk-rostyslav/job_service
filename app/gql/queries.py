from graphene import ObjectType, List, Int, Field
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject
from app.db.database import get_async_session
from app.db.models import Job, Employer, User, JobApplication
from app.utils import admin_user
from sqlalchemy import select, outerjoin


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id = Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id = Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)

    @staticmethod
    async def resolve_job(root, info, id):
        session = await get_async_session()
        result = await session.execute(select(Job).where(Job.id == id))
        job = result.scalars().first()
        await session.close()
        return job

    @staticmethod
    async def resolve_jobs(root, info):
        session = await get_async_session()
        result = await session.execute(select(Job))
        jobs = result.scalars().fetchall()
        await session.close()
        return jobs


    @staticmethod
    async def resolve_employer(root, info, id):
        session = await get_async_session()
        result = await session.execute(select(Employer).where(Employer.id == id))
        employers = result.scalars().first()
        await session.close()
        return employers

    @staticmethod
    async def resolve_employers(root, info):
        session = await get_async_session()
        result = await session.execute(select(Employer))
        employers = result.scalars().all()
        await session.close()
        return employers


    @staticmethod
    async def resolve_users(root, info):
        session = await get_async_session()
        result = await session.execute(select(User))
        users = result.scalars().all()
        await session.close()
        return users


    @admin_user
    async def resolve_job_applications(root, info):
        session = await get_async_session()
        result = await session.execute(select(JobApplication))
        applications = result.scalars().all()
        await session.close()
        return applications
