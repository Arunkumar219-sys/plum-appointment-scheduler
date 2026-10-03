import pytest
from app.services.pipeline import pipeline_service

def test_valid_text_appointment():
    # Assignment example 1
    sample_text = "Book dentist next Friday at 3pm"
    ref_date = "2025-09-20"
    
    result, status_code = pipeline_service.process_text_request(sample_text, ref_date)
    
    assert status_code == 200
    assert result["status"] == "ok"
    assert result["appointment"]["department"] == "Dentistry"
    assert result["appointment"]["date"] == "2025-09-26"
    assert result["appointment"]["time"] == "15:00"
    assert result["appointment"]["tz"] == "Asia/Kolkata"

def test_ocr_noisy_text_appointment():
    # Assignment OCR sample
    sample_text = "book dentist nxt Friday @ 3 pm"
    ref_date = "2025-09-20"
    
    result, status_code = pipeline_service.process_text_request(sample_text, ref_date)
    
    assert status_code == 200
    assert result["status"] == "ok"
    assert result["appointment"]["department"] == "Dentistry"
    assert result["appointment"]["date"] == "2025-09-26"
    assert result["appointment"]["time"] == "15:00"

def test_ambiguous_guardrail_trigger():
    # Ambiguous date and missing department
    sample_text = "book appointment sometime later"
    
    result, status_code = pipeline_service.process_text_request(sample_text)
    
    assert status_code == 400
    assert result["status"] == "needs_clarification"
    assert result["message"] == "Ambiguous date/time or department"

def test_missing_department_guardrail():
    # Missing medical department
    sample_text = "Book next Friday at 3pm"
    
    result, status_code = pipeline_service.process_text_request(sample_text)
    
    assert status_code == 400
    assert result["status"] == "needs_clarification"

def test_dermatology_appointment():
    sample_text = "Schedule derma appointment tomorrow at 10am"
    result, status_code = pipeline_service.process_text_request(sample_text)
    
    assert status_code == 200
    assert result["status"] == "ok"
    assert result["appointment"]["department"] == "Dermatology"
    assert result["appointment"]["time"] == "10:00"
