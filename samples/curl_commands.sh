#!/bin/bash

# Base URL (Change to your ngrok URL or localhost)
BASE_URL="http://localhost:8000"

echo "=========================================="
echo "1. Health Check Endpoint"
echo "=========================================="
curl -X GET "$BASE_URL/api/v1/health" \
     -H "Accept: application/json"
echo -e "\n"

echo "=========================================="
echo "2. Typed Text Appointment Request (Assignment Spec Sample)"
echo "=========================================="
curl -X POST "$BASE_URL/api/v1/schedule/text" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Book dentist next Friday at 3pm",
       "reference_date": "2025-09-20"
     }'
echo -e "\n"

echo "=========================================="
echo "3. Ambiguous Text Request (Guardrail Trigger)"
echo "=========================================="
curl -X POST "$BASE_URL/api/v1/schedule/text" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Book appointment next week"
     }'
echo -e "\n"

echo "=========================================="
echo "4. Image Upload Request (OCR Pipeline)"
echo "=========================================="
curl -X POST "$BASE_URL/api/v1/schedule/image" \
     -F "file=@samples/sample_appointment_note.png" \
     -F "reference_date=2025-09-20"
echo -e "\n"
