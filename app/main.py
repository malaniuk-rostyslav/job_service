from graphene import Schema
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import prepare_database
from app.gql.queries import Query
from app.db.database import Session
from app.db.models import Employer, Job

schema = Schema(query=Query)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield prepare_database()


app = FastAPI(lifespan=app_lifespan)


@app.get("/employers")
def get_employers():
    with Session() as session:
        employers = session.query(Employer).all()
        return employers


@app.get("/jobs")
def get_jobs():
    with Session() as session:
        jobs = session.query(Job).all()
        return jobs


app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))
