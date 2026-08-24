from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from query_generator import generate_sql
from db import run_query, UnsafeQueryError

app = FastAPI(title="NL-to-SQL Analytics (Stage 1)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    sql: str
    explanation: str
    columns: list[str]
    rows: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    generated = generate_sql(req.question)
    sql = generated["sql"]
    explanation = generated["explanation"]

    if not sql:
        raise HTTPException(status_code=422, detail=explanation or "Could not generate SQL for this question.")

    try:
        result = run_query(sql)
    except UnsafeQueryError as e:
        raise HTTPException(status_code=400, detail=f"Rejected unsafe query: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {e}")

    return AskResponse(
        question=req.question,
        sql=sql,
        explanation=explanation,
        columns=result["columns"],
        rows=result["rows"],
    )
