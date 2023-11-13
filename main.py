from fastapi import FastAPI
from routes.route import router

app = FastAPI()

from pymongo.mongo_client import MongoClient

app.include_router(router)
