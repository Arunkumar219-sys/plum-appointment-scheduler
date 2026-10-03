from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## Plum SDE Intern Assignment - Problem Statement 1
    ### AI-Powered Appointment Scheduler Assistant

    * **Focus Area**: OCR -> Entity Extraction -> Normalization
    * **Features**:
      - Handles typed natural language requests (`/api/v1/schedule/text`)
      - Handles uploaded images/notes with OCR (`/api/v1/schedule/image`)
      - Normalizes relative date/time into ISO format (`Asia/Kolkata`)
      - Implements guardrails for ambiguous inputs
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local testing & ngrok
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
