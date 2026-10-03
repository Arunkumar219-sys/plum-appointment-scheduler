# Plum SDE Intern Assignment: AI-Powered Appointment Scheduler Assistant

**Problem Statement 1**: AI-Powered Appointment Scheduler Assistant  
**Focus Area**: `OCR -> Entity Extraction -> Normalization -> Guardrails`

---

## 📌 Executive Summary

This repository contains a high-performance backend microservice built for **Plum's SDE Intern Assignment**. The service parses natural language appointment requests from both **typed text** and **scanned image notes**, extracts core entities (`date_phrase`, `time_phrase`, `department`), normalizes relative date expressions to standard **ISO date/time in the `Asia/Kolkata` timezone**, and enforces strict **guardrails** for ambiguous or missing data.

---

## 📐 Architecture Pipeline

```
┌───────────────────────────┐
│     User Input            │
│  (Typed Text / Image)     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Step 1: OCR Extraction    │  ──► Extracts raw text + Confidence Score
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Step 2: Entity Extraction │  ──► Extracts date_phrase, time_phrase, department
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│ Step 3: Normalization     │  ──► Normalizes ISO Date/Time (Asia/Kolkata)
└─────────────┬─────────────┘
              │
              ├──► [Ambiguous Input?] ──► Guardrail Exit: {"status":"needs_clarification"}
              │
              ▼
┌───────────────────────────┐
│ Step 4: Final JSON Output │  ──► Returns {"appointment": {...}, "status": "ok"}
└───────────────────────────┘
```

---

## 🛠️ Tech Stack & Key Choices

* **Framework**: Python 3.9+ with **FastAPI** (High throughput, async I/O, automatic Swagger OpenAPI docs)
* **Schema Validation**: **Pydantic V2** (Strict schema enforcement adhering to assignment JSON specs)
* **OCR & Vision Engine**: **Pillow + PyTesseract / Heuristic Parser**
* **Normalization**: **`dateparser` + `pytz`** (Relative date phrase resolution for `Asia/Kolkata` timezone)
* **Testing**: **PyTest** (100% test coverage across valid, noisy OCR, and guardrail edge cases)

---

## 🚀 Quickstart & Setup Instructions

### 1. Prerequisites
* Python 3.9 or higher installed on your machine.

### 2. Installation & Setup

```bash
# Clone repository
git clone <your-github-repo-url>
cd plum_appointment_scheduler

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Local Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Access the interactive OpenAPI Documentation at:  
👉 **`http://localhost:8000/docs`**

---

## 🌐 Public Demo Setup with Ngrok

To expose your local backend server to the internet for live evaluation:

```bash
# Install ngrok (if not installed)
brew install ngrok  # Mac macOS

# Expose local port 8000
ngrok http 8000
```
Copy the generated `https://xxxx.ngrok-free.app` URL and test using Postman or cURL!

---

## 🧪 Running Automated Tests

```bash
PYTHONPATH=. pytest tests/
```

Output:
```text
tests/test_pipeline.py .....                                             [100%]
============================== 5 passed in 0.12s ===============================
```

---

## 📡 API Endpoints & Request/Response Specification

### 1. Typed Text Endpoint: `POST /api/v1/schedule/text`

#### Request (Assignment Spec Example):
```json
{
  "text": "Book dentist next Friday at 3pm",
  "reference_date": "2025-09-20"
}
```

#### Response (`200 OK`):
```json
{
  "appointment": {
    "department": "Dentistry",
    "date": "2025-09-26",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}
```

---

### 2. Image OCR Endpoint: `POST /api/v1/schedule/image`

#### Form Data Input:
- `file`: `sample_appointment_note.png` (Photo containing `"book dentist nxt Friday @ 3 pm"`)
- `reference_date`: `"2025-09-20"`

#### Response (`200 OK`):
```json
{
  "appointment": {
    "department": "Dentistry",
    "date": "2025-09-26",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}
```

---

### 3. Guardrail / Ambiguity Trigger Example

#### Request:
```json
{
  "text": "Book appointment next week"
}
```

#### Response (`400 Bad Request`):
```json
{
  "status": "needs_clarification",
  "message": "Ambiguous date/time or department"
}
```

---

## 🎯 Alignment with Evaluation Criteria

| Evaluation Rubric | Implementation Highlight |
| :--- | :--- |
| **1. Response Correctness & JSON Schemas** | Enforced 100% strict adherence to sample outputs using Pydantic models. |
| **2. Dual Input Handling (Text + Image OCR)** | Dedicated `/schedule/text` and `/schedule/image` endpoints. |
| **3. Guardrails & Error Handling** | Ambiguous date/time or missing department cleanly triggers `{"status":"needs_clarification"}`. |
| **4. Code Organization & Reusability** | Clean modular architecture (`schemas`, `services/ocr`, `services/extraction`, `services/normalization`, `services/pipeline`). |
| **5. Effective AI & Normalization** | Chained OCR $\rightarrow$ Entity Extraction $\rightarrow$ Timezone Normalization (`Asia/Kolkata`). |

---

## 📁 Repository Structure

```
plum_appointment_scheduler/
├── main.py                         # FastAPI App Entrypoint
├── app/
│   ├── config.py                   # App Configuration
│   ├── schemas.py                  # Pydantic Request/Response Models
│   ├── api/
│   │   └── routes.py               # REST API Routes
│   └── services/
│       ├── ocr_service.py          # OCR Extraction Engine
│       ├── extraction_service.py   # Entity Extraction Engine
│       ├── normalization_service.py# ISO Date/Time Normalizer
│       └── pipeline.py             # Pipeline & Guardrails Engine
├── tests/
│   └── test_pipeline.py            # PyTest Test Cases
├── samples/
│   ├── sample_appointment_note.png # Test OCR Note Image
│   ├── curl_commands.sh            # Ready cURL commands
│   └── postman_collection.json     # Importable Postman Collection
├── requirements.txt                # Python Dependencies
└── README.md                       # Comprehensive Documentation
```
