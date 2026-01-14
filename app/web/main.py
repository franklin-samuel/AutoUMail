from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from app.web.controller import email_controller

app = FastAPI(
    title="AutoUMail Service",
    description="Sistema de classificação automática de emails com IA",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(email_controller.router)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        "not-found.html",
        {"request": request},
        status_code=404
    )