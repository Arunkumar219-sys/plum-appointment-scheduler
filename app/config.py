import os

class Settings:
    PROJECT_NAME: str = "Plum AI-Powered Appointment Scheduler Assistant"
    VERSION: str = "1.0.0"
    DEFAULT_TIMEZONE: str = "Asia/Kolkata"
    
    # AI API Keys (Optional - System automatically falls back to Deterministic NLP Engine if not provided)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
