from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.models.llm_agent import analyze_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Guardian API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class TextPayload(BaseModel):
    text: str

@app.post("/analyze")
def analyze(payload: TextPayload):
    try:
        result = analyze_text(payload.text)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"msg": "AI Guardian API running"}
