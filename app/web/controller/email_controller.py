from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.business.email_classifier_port import EmailClassifierPort
from app.core.business.read_file_port import ReadFilePort
from app.domain.email import Email
from app.domain.exception.business_exception import BusinessException
from app.web.model.classify_email_request import ClassifyEmailFileRequest, ClassifyEmailTextRequest
from app.web.dependency import get_email_classifier_port, get_read_file_port

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/classifier", response_class=HTMLResponse)
async def classifier_page(request: Request):
    return templates.TemplateResponse("classifier.html", {"request": request})


@router.post("/api/classify/file")
async def classify_file(
        request: Request,
        form: Annotated[ClassifyEmailFileRequest, Depends()],
        email_classifier: Annotated[EmailClassifierPort, Depends(get_email_classifier_port)],
        file_reader: Annotated[ReadFilePort, Depends(get_read_file_port)]
):
    try:
        content = await file_reader.read(form.file)
        if not content:
            raise BusinessException("Por favor, anexe o arquivo.")

        email = Email(original_content=content, processed_content=None)

        classification = await email_classifier.classify(email)

        return JSONResponse({
            "success": True,
            "category": classification.category.value,
            "suggested_response": classification.suggested_response
        })

    except BusinessException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/classify/text")
async def classify_text(
        request: Request,
        form: Annotated[ClassifyEmailTextRequest, Depends()],
        email_classifier: Annotated[EmailClassifierPort, Depends(get_email_classifier_port)]
):
    try:
        if form.text is None:
            raise BusinessException('Por favor, digite ou cole o texto do email.')

        content = form.text.strip()

        if not content:
            raise BusinessException("Por favor, digite ou cole o texto do email.")

        email = Email(original_content=content, processed_content=None)

        classification = await email_classifier.classify(email)

        return JSONResponse({
            "success": True,
            "category": classification.category.value,
            "suggested_response": classification.suggested_response
        })

    except BusinessException as e:
        raise HTTPException(status_code=400, detail=str(e))
