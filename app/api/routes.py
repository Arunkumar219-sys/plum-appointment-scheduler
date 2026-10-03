from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from typing import Optional
from app.schemas import TextRequest, SuccessfulAppointmentResponse, ClarificationResponse
from app.services.pipeline import pipeline_service

router = APIRouter(prefix="/api/v1", tags=["Appointment Scheduler"])

@router.get("/health", summary="API Health Check")
def health_check():
    return {"status": "healthy", "service": "Plum AI Appointment Scheduler API"}

@router.post(
    "/schedule/text",
    summary="Schedule appointment from typed text",
    description="Parses natural language typed appointment requests, extracts entities, normalizes ISO date/time, and enforces guardrails."
)
def schedule_text(payload: TextRequest):
    result, status_code = pipeline_service.process_text_request(
        text=payload.text,
        reference_date_str=payload.reference_date
    )
    return result

@router.post(
    "/schedule/image",
    summary="Schedule appointment from uploaded image note",
    description="Parses photo of handwritten notes or emails using OCR, extracts entities, normalizes ISO date/time, and returns final JSON."
)
async def schedule_image(
    file: UploadFile = File(..., description="Uploaded image note (PNG/JPEG)"),
    reference_date: Optional[str] = Form(None, description="Optional reference date YYYY-MM-DD")
):
    if not file.content_type.startswith("image/") and not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided is not a valid image."
        )

    image_bytes = await file.read()
    result, status_code = pipeline_service.process_image_request(
        image_bytes=image_bytes,
        filename=file.filename,
        reference_date_str=reference_date
    )
    return result
