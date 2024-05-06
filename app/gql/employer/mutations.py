from graphene import Mutation, String, Field, Int, Boolean
from graphql import GraphQLError
from app.gql.types import EmployerObject
from app.db.database import get_async_session
from app.db.models import Employer
from app.utils import admin_user
from sqlalchemy import select


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(EmployerObject)

    @admin_user
    async def mutate(root, info, name, contact_email, industry):
        session = await get_async_session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        await session.commit()
        await session.refresh(employer)
        await session.close()
        return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(EmployerObject)

    @admin_user
    async def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):
        session = await get_async_session()
        result = await session.execute(select(Employer).where(Employer.id == employer_id))
        employer = result.scalars().first()

        if not employer:
            raise GraphQLError("Employer not found")

        if name:
            employer.name = name
        if contact_email:
            employer.contact_email = contact_email
        if industry:
            employer.industry = industry

        await session.commit()
        await session.refresh(employer)
        await session.close()
        return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)

    success = Boolean()

    @admin_user
    async def mutate(root, info, employer_id):
        session = await get_async_session()
        result = await session.execute(select(Employer).where(Employer.id == employer_id))
        employer = result.scalars().first()

        if not employer:
            raise GraphQLError("Employer not found")
            
        await session.delete(employer)
        await session.commit()
        await session.close()
        return DeleteEmployer(success=True)
