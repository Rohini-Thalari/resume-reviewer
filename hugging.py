from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import json
import io
import re

load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found in .env file")

client = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct",
    token=API_KEY
)

app = FastAPI(title="AI Resume Reviewer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def frontend():
    with open("index.html") as f:
        return f.read()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid PDF file")


def extract_json_from_reply(reply: str) -> dict:
    reply = re.sub(r"```json|```", "", reply).strip()
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise HTTPException(
        status_code=500,
        detail=f"LLM returned invalid JSON. Raw: {reply[:400]}"
    )

SYSTEM_PROMPT = """You are a STRICT ATS Resume Evaluator.

You will receive:
- Job Role
- Required Experience (in years)
- Resume Content

Evaluation Rules:

1. Role Alignment:
   - Resume must match the core technical domain of the Job Role.
   - If core technologies required for the role are missing → final_verdict = "Weak".

2. Experience Validation:
   - If Required Experience > candidate's demonstrated experience → downgrade verdict.
   - Fresher resume must NOT get "Strong" for senior roles.

3. Skill Gap Identification:
   - Identify exactly 4 important missing tools/technologies required for the Job Role.
   - Only list real missing tools. Do NOT invent skills already present.

4. Improvement Suggestions:
   - Provide exactly 3 or 5 concrete suggestions.
   - Suggestions must include specific project ideas aligned with the Job Role.
   - No generic advice.

Return ONLY valid JSON:

{
  "skill_gaps": ["tool1", "tool2", "tool3", "tool4"],
  "improvement_suggestions": ["suggestion1", "suggestion2", "suggestion3"],
  "final_verdict": "Strong" or "Average" or "Weak"
}

No explanation. No markdown. Only JSON."""

@app.post("/analyze")
async def analyze(
    job_role: str = Form(...),
    experience: str = Form(...),
    resume_file: UploadFile = File(...)
):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Resume must be PDF")

    resume_bytes = await resume_file.read()
    resume_text = extract_text_from_pdf(resume_bytes)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text")

    # Limit resume to avoid overflow but keep enough context
    resume_text = resume_text[:3000]

    response = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Job Role: {job_role}\nRequired Experience: {experience} years\n\nResume:\n{resume_text}"}
        ],
        max_tokens=600,
        temperature=0.1
    )

    reply = response.choices[0].message.content.strip()
    result = extract_json_from_reply(reply)

    return JSONResponse(content={
        "skill_gaps": result.get("skill_gaps", []),
        "improvement_suggestions": result.get("improvement_suggestions", []),
        "final_verdict": result.get("final_verdict", "Weak")
    })
