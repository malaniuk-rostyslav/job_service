from graphene import Schema
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import prepare_database
from app.gql.queries import Query
from app.gql.mutations import Mutation
from app.db.database import Session
from app.db.models import Employer, Job

schema = Schema(query=Query, mutation=Mutation)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield prepare_database()


app = FastAPI(lifespan=app_lifespan)


app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))
