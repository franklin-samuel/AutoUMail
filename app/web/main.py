import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
import logging

from app.domain.exception.business_exception import BusinessException

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from app.web.controller import email_controller

app = FastAPI(
    title="AutoUMail Service",
    description="Sistema de classificação automática de emails com IA",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(email_controller.router)


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    logger.warning(f"Business Error: {exc.message}")

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "detail": str(exc.message)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": "Ocorreu um erro interno. Tente novamente mais tarde."
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        "not-found.html",
        {"request": request},
        status_code=404
    )

if __name__ == "__main__":
    uvicorn.run(
        "web.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )