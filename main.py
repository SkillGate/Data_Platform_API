from fastapi import FastAPI
from routes.route import router
from fastapi.responses import HTMLResponse

app = FastAPI()

app.include_router(router)

