import re
from typing import Dict, Any, Tuple, Optional
from app.schemas import EntityDetails, EntityExtractionStep

# Recognized medical departments / specialties dictionary
DEPARTMENT_MAPPING = {
    "dentist": "Dentistry",
    "dental": "Dentistry",
    "dentistry": "Dentistry",
    "derma": "Dermatology",
    "dermatologist": "Dermatology",
    "dermatology": "Dermatology",
    "skin": "Dermatology",
    "cardio": "Cardiology",
    "cardiologist": "Cardiology",
    "cardiology": "Cardiology",
    "heart": "Cardiology",
    "ortho": "Orthopedics",
    "orthopedics": "Orthopedics",
    "orthopedist": "Orthopedics",
    "bone": "Orthopedics",
    "physician": "General Physician",
    "doctor": "General Physician",
    "gp": "General Physician",
    "eye": "Ophthalmology",
    "ophthalmologist": "Ophthalmology",
    "pediatrician": "Pediatrics",
    "pediatrics": "Pediatrics",
    "ent": "ENT (Ear, Nose, Throat)",
    "neurologist": "Neurology"
}

class EntityExtractionService:
    """
    Extracts date_phrase, time_phrase, and department from raw text.
    Handles typos, abbreviations (e.g. 'nxt' -> 'next', '@ 3 pm' -> '3pm').
    """

    @staticmethod
    def extract_entities(raw_text: str) -> EntityExtractionStep:
        text_lower = raw_text.lower()

        # 1. Extract Department
        department_found: Optional[str] = None
        for keyword in sorted(DEPARTMENT_MAPPING.keys(), key=len, reverse=True):
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                department_found = keyword
                break

        # 2. Extract Time Phrase
        # Regex patterns for time phrases like "3pm", "3 pm", "15:00", "at 3pm", "10:30 am", "@ 3 pm"
        time_pattern = r'(@\s*\d{1,2}(?::\d{2})?\s*(?:am|pm)?|\b\d{1,2}(?::\d{2})?\s*(?:am|pm)\b|\bat\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?\b|\b\d{1,2}:\d{2}\b)'
        time_match = re.search(time_pattern, text_lower)
        
        time_phrase: Optional[str] = None
        if time_match:
            raw_time_str = time_match.group(0)
            # clean leading '@' or 'at'
            cleaned_time = re.sub(r'^(?:@|at)\s*', '', raw_time_str).strip()
            time_phrase = cleaned_time

        # 3. Extract Date Phrase
        # Look for phrases like "next Friday", "this Friday", "nxt Friday", "tomorrow", "today", "in 3 days", "on 2025-09-26"
        date_pattern = r'\b((?:next|nxt|this|coming)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|tomorrow|today|in\s+\d+\s+days|\d{4}-\d{2}-\d{2}|\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*)\b'
        date_match = re.search(date_pattern, text_lower)

        date_phrase: Optional[str] = None
        if date_match:
            raw_date_str = date_match.group(0)
            # Normalize common OCR typos in date phrase
            raw_date_str = re.sub(r'\bnxt\b', 'next', raw_date_str)
            date_phrase = raw_date_str

        # Calculate confidence
        found_count = sum(1 for item in [date_phrase, time_phrase, department_found] if item is not None)
        confidence = round(0.50 + (found_count * 0.15), 2)
        if found_count == 3:
            confidence = 0.85

        entities = EntityDetails(
            date_phrase=date_phrase,
            time_phrase=time_phrase,
            department=department_found
        )

        return EntityExtractionStep(
            entities=entities,
            entities_confidence=confidence
        )

extraction_service = EntityExtractionService()
