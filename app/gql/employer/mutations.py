from graphene import Mutation, String, Field, Int, Boolean
from graphql import GraphQLError
from app.gql.types import EmployerObject
from app.db.database import Session
from app.db.models import Employer
from app.utils import admin_user

class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(EmployerObject)

    @admin_user
    def mutate(root, info, name, contact_email, industry):
        with Session() as session:
            employer = Employer(name=name, contact_email=contact_email, industry=industry)
            session.add(employer)
            session.commit()
            session.refresh(employer)
            return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(EmployerObject)

    @admin_user
    def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):
        with Session() as session:
            employer = session.query(Employer).filter(Employer.id==employer_id).first()

            if not employer:
                raise GraphQLError("Employer not found")

            if name:
                employer.name = name
            if contact_email:
                employer.contact_email = contact_email
            if industry:
                employer.industry = industry

            session.commit()
            session.refresh(employer)
        return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @admin_user
    def mutate(root, info, id):
        with Session() as session:
            employer = session.query(Employer).filter(Employer.id==id).first()

            if not employer:
                raise GraphQLError("Employer not found")
            
            session.delete(employer)
            session.commit()
            return DeleteEmployer(success=True)
