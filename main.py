from fastapi import FastAPI
from routes.settings import router as settings_router
from routes.shifts import router as shift_router
from fastapi.responses import FileResponse
from storage.database import init_db



app = FastAPI()
init_db()


@app.get("/")
def serve_mini_app():
    return FileResponse("miniapp/index.html")

app.include_router(settings_router)
app.include_router(shift_router)