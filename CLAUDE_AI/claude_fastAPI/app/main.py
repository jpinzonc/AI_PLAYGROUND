from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .models import ProjectData

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    project_data = ProjectData()
    return templates.TemplateResponse("dashboard.html", {"request": request, "project": project_data})

@app.get("/api/project-data")
async def get_project_data():
    return ProjectData()