from graphene import Schema
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import init_db
from app.gql.queries import Query
from app.gql.mutations import Mutation

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
