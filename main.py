from fastapi import FastAPI
from routes.route import router

app = FastAPI()

from pymongo.mongo_client import MongoClient

app.include_router(router)

# uri = "mongodb+srv://admin:1234@cluster0.hxusbsq.mongodb.net/?retryWrites=true&w=majority"

# # Create a new client and connect to the server
# client = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)