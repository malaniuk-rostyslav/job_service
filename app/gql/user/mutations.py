from graphene import Mutation, String, Field, Int
from graphql import GraphQLError
from app.db.database import get_async_session
from app.db.models import User, JobApplication, Job
from app.utils import generate_token, verify_password, hash_password, get_authenticated_user, auth_user_same_as
from app.gql.types import UserObject, JobApplicationObject
from sqlalchemy import select, exists


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)
    
    token = String()

    @staticmethod
    async def mutate(root, info, email, password):
        session = await get_async_session()
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        await session.close()

        if not user:
            raise GraphQLError("User by this email does not exist")
        
        await verify_password(user.password_hash, password)
        
        token = await generate_token(email)

        return LoginUser(token=token)
    

class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(UserObject)

    @staticmethod
    async def mutate(root, info, username, email, password, role):
        if role == 'admin':
            current_user = get_authenticated_user(info.context)
            if current_user.role != "admin":
                raise GraphQLError("Only admin users can add new admin users")
        session = await get_async_session()
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            raise GraphQLError("A user with this email already exists")
        password_hash = await hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        await session.close()
        return AddUser(user=user)


class ApplyToJob(Mutation):
    class Arguments:
        user_id = Int()
        job_id = Int()

    job_application = Field(JobApplicationObject)

    @auth_user_same_as
    async def mutate(root, info, user_id, job_id):
        session = await get_async_session()
        user_applied = await session.execute(
            select(
                exists().where(
                    JobApplication.user_id == user_id,
                    JobApplication.job_id == job_id
                )
            )
        )
        if user_applied.scalar():
            raise GraphQLError("This user has already applied to this job")
        
        job_exists = await session.execute(
            select(
                exists().where(
                    Job.id == job_id
                )
            )
        )

        if not job_exists.scalar():
            raise GraphQLError("Job does not exist")
        
        job_application = JobApplication(user_id=user_id, job_id=job_id)
        session.add(job_application)
        await session.commit()
        await session.refresh(job_application)
        await session.close()
        return ApplyToJob(job_application=job_application)