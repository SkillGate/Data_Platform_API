from fastapi import FastAPI
from routes.route import router
from fastapi.responses import HTMLResponse

app = FastAPI()

app.include_router(router)

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            wellcome
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)