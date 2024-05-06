from graphene import Mutation, String, Field, Int
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User, JobApplication
from app.utils import generate_token, verify_password, hash_password, get_authenticated_user, auth_user_same_as
from app.gql.types import UserObject, JobApplicationObject


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)
    
    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("User by this email does not exist")
        
        verify_password(user.password_hash, password)
        
        token = generate_token(email)

        return LoginUser(token=token)
    

class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(UserObject)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        if role == 'admin':
            current_user = get_authenticated_user(info.context)
            if current_user.role != "admin":
                raise GraphQLError("Only admin users can add new admin users")
        with Session() as session:
            user = session.query(User).filter(User.email==email).first()
            if user:
                raise GraphQLError("A user with this email already exists")
            password_hash = hash_password(password)
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role)
            session.add(user)
            session.commit()
            session.refresh(user)
            return AddUser(user=user)


class ApplyToJob(Mutation):
    class Arguments:
        user_id = Int()
        job_id = Int()

    job_application = Field(JobApplicationObject)

    @auth_user_same_as
    def mutate(root, info, user_id, job_id):
        with Session() as session:
            job = session.query(
                session.query(JobApplication)
                .filter(
                    JobApplication.user_id==user_id,
                    JobApplication.job_id==job_id
                )
            .exists()).scalar()
            if job:
                raise GraphQLError("This user has already applied to this job")
            
            job_application = JobApplication(user_id=user_id, job_id=job_id)
            session.add(job_application)
            session.commit()
            session.refresh(job_application)
            return ApplyToJob(job_application=job_application)