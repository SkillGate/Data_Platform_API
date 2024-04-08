from fastapi import FastAPI, __version__
from routes.route import router

app = FastAPI()

from pymongo.mongo_client import MongoClient

app.include_router(router)
