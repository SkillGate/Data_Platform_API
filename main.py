from fastapi import FastAPI
from routes.route import router
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for your setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
