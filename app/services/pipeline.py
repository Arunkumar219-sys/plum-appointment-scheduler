from datetime import datetime, date
from typing import Dict, Any, Optional, Tuple
from app.schemas import (
    OCRExtractionStep,
    EntityExtractionStep,
    NormalizationStep,
    SuccessfulAppointmentResponse,
    ClarificationResponse,
    AppointmentDetails,
    FullPipelineResponse
)
from app.services.ocr_service import ocr_service
from app.services.extraction_service import extraction_service, DEPARTMENT_MAPPING
from app.services.normalization_service import normalization_service

class AppointmentPipeline:
    """
    Complete Pipeline Orchestrator for Problem Statement 1:
    OCR -> Entity Extraction -> Normalization -> Guardrails & Final JSON
    """

    @staticmethod
    def process_text_request(text: str, reference_date_str: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """
        Processes typed text appointment requests.
        Returns (JSON_Response, HTTP_Status_Code).
        """
        # Parse reference date if provided
        ref_date = date.today()
        if reference_date_str:
            try:
                ref_date = datetime.strptime(reference_date_str, "%Y-%m-%d").date()
            except ValueError:
                pass

        # Step 1: OCR / Text Input Step
        ocr_step = OCRExtractionStep(
            raw_text=text,
            confidence=0.90
        )

        # Step 2: Entity Extraction
        entities_step = extraction_service.extract_entities(text)

        # Step 3: Normalization & Guardrail Check
        normalized_details, norm_confidence, is_valid, error_msg = normalization_service.normalize_entities(
            entities_step.entities, ref_date=ref_date
        )

        if not is_valid or not normalized_details or not entities_step.entities.department:
            # Guardrail / Exit Condition
            clarification = ClarificationResponse(
                status="needs_clarification",
                message="Ambiguous date/time or department"
            )
            return clarification.model_dump(), 400

        norm_step = NormalizationStep(
            normalized=normalized_details,
            normalization_confidence=norm_confidence
        )

        # Map department keyword to standardized Medical Specialty name
        raw_dept = entities_step.entities.department.lower()
        std_department = DEPARTMENT_MAPPING.get(raw_dept, raw_dept.capitalize())

        # Step 4: Final Appointment JSON
        appointment_res = SuccessfulAppointmentResponse(
            appointment=AppointmentDetails(
                department=std_department,
                date=normalized_details.date,
                time=normalized_details.time,
                tz=normalized_details.tz
            ),
            status="ok"
        )

        return appointment_res.model_dump(), 200

    @staticmethod
    def process_image_request(image_bytes: bytes, filename: str = "", reference_date_str: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
        """
        Processes image appointment requests (scanned notes, emails, handwritten receipts).
        """
        # Step 1: OCR Extraction from Image
        raw_text, ocr_confidence = ocr_service.extract_text_from_image(image_bytes, filename)

        if not raw_text or len(raw_text.strip()) == 0:
            clarification = ClarificationResponse(
                status="needs_clarification",
                message="Ambiguous date/time or department"
            )
            return clarification.model_dump(), 400

        # Pass extracted text to full pipeline
        return AppointmentPipeline.process_text_request(raw_text, reference_date_str)

pipeline_service = AppointmentPipeline()
