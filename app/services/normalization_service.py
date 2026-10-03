from datetime import datetime, date, timedelta
import dateparser
import pytz
from typing import Optional, Tuple, Dict, Any
from app.schemas import EntityDetails, NormalizedDetails, NormalizationStep

TIMEZONE = "Asia/Kolkata"

class NormalizationService:
    """
    Normalizes extracted date and time phrases into ISO standards for Asia/Kolkata timezone.
    Triggers guardrail if information is ambiguous or missing.
    """

    @staticmethod
    def normalize_entities(entities: EntityDetails, ref_date: Optional[date] = None) -> Tuple[Optional[NormalizedDetails], float, bool, str]:
        """
        Returns (NormalizedDetails, confidence, is_valid, error_message)
        """
        date_phrase = entities.date_phrase
        time_phrase = entities.time_phrase
        dept = entities.department

        # Guardrail check 1: Check missing core entities
        if not date_phrase or not time_phrase or not dept:
            return None, 0.0, False, "Ambiguous date/time or department"

        if ref_date is None:
            # Default reference date if none passed
            ref_date = date.today()

        ref_datetime = datetime.combine(ref_date, datetime.min.time())

        # 1. Normalize Date
        parsed_date_str: Optional[str] = None
        
        # Custom logic for "next <weekday>" or "nxt <weekday>"
        cleaned_date_phrase = date_phrase.lower().replace("nxt", "next")
        
        if "next" in cleaned_date_phrase:
            weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            for idx, day_name in enumerate(weekdays):
                if day_name in cleaned_date_phrase:
                    current_weekday = ref_date.weekday() # 0 = Mon, 4 = Fri, 5 = Sat
                    days_ahead = (idx - current_weekday) % 7
                    if days_ahead == 0:
                        days_ahead = 7
                    target_date = ref_date + timedelta(days=days_ahead)
                    parsed_date_str = target_date.strftime("%Y-%m-%d")
                    break

        if not parsed_date_str:
            # Try dateparser
            dt_parsed = dateparser.parse(
                cleaned_date_phrase,
                settings={'RELATIVE_BASE': ref_datetime, 'PREFER_DATES_FROM': 'future'}
            )
            if dt_parsed:
                parsed_date_str = dt_parsed.strftime("%Y-%m-%d")

        if not parsed_date_str:
            return None, 0.0, False, "Ambiguous date/time or department"

        # 2. Normalize Time
        parsed_time_str: Optional[str] = None
        cleaned_time_phrase = time_phrase.lower().strip()

        dt_time_parsed = dateparser.parse(cleaned_time_phrase)
        if dt_time_parsed:
            parsed_time_str = dt_time_parsed.strftime("%H:%M")

        if not parsed_time_str:
            return None, 0.0, False, "Ambiguous date/time or department"

        normalized = NormalizedDetails(
            date=parsed_date_str,
            time=parsed_time_str,
            tz=TIMEZONE
        )

        return normalized, 0.90, True, ""

normalization_service = NormalizationService()
