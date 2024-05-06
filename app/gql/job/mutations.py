from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.gql.types import JobObject
from app.db.database import get_async_session
from app.db.models import Job
from app.utils import admin_user
from sqlalchemy import select


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(JobObject)

    @admin_user
    async def mutate(root, info, title, description, employer_id):
        session = await get_async_session()
        job = Job(title=title, description=description, employer_id=employer_id)
        session.add(job)
        await session.commit()
        await session.refresh(job)
        await session.close()
        return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(JobObject)

    @admin_user
    async def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        session = await get_async_session()
        result = await session.execute(select(Job).where(Job.id == job_id))
        job = result.scalars().first()

        if not job:
            raise GraphQLError("Job not found")

        if title:
            job.title = title
        if description:
            job.description = description
        if employer_id:
            job.employer_id = employer_id

        await session.commit()
        await session.refresh(job)
        await session.close()
        return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        job_id = Int(required=True)

    success = Boolean()

    @admin_user
    async def mutate(root, info, job_id):
        session = await get_async_session()
        result = await session.execute(select(Job).where(Job.id == job_id))
        job = result.scalars().first()

        if not job:
            raise GraphQLError("Job not found")
            
        session.delete(job)
        session.commit()
        await session.close()
        return DeleteJob(success=True)
