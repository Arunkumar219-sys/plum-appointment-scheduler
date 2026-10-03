from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class TextRequest(BaseModel):
    text: str = Field(..., json_schema_extra={"example": "Book dentist next Friday at 3pm"}, description="Raw appointment request text")
    reference_date: Optional[str] = Field(None, json_schema_extra={"example": "2025-09-20"}, description="Optional ISO reference date YYYY-MM-DD for date phrase resolution")

class OCRExtractionStep(BaseModel):
    raw_text: str
    confidence: float

class EntityDetails(BaseModel):
    date_phrase: Optional[str] = None
    time_phrase: Optional[str] = None
    department: Optional[str] = None

class EntityExtractionStep(BaseModel):
    entities: EntityDetails
    entities_confidence: float

class NormalizedDetails(BaseModel):
    date: Optional[str] = None  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM (24h)
    tz: str = "Asia/Kolkata"

class NormalizationStep(BaseModel):
    normalized: Optional[NormalizedDetails] = None
    normalization_confidence: float

class AppointmentDetails(BaseModel):
    department: str
    date: str
    time: str
    tz: str = "Asia/Kolkata"

class ClarificationResponse(BaseModel):
    status: str = "needs_clarification"
    message: str = "Ambiguous date/time or department"

class SuccessfulAppointmentResponse(BaseModel):
    appointment: AppointmentDetails
    status: str = "ok"

class FullPipelineResponse(BaseModel):
    status: str
    step_1_ocr: OCRExtractionStep
    step_2_entities: Optional[EntityExtractionStep] = None
    step_3_normalized: Optional[NormalizationStep] = None
    step_4_final: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
