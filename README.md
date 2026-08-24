# NL-to-SQL Analytics — Stage 1

A minimal working pipeline: ask a question in plain English, get back SQL,
results, and a plain-English explanation. This is Stage 1 of the full build
(hardcoded schema, basic pipeline, no retrieval/eval yet — those come in
later stages).

## What's here

- `backend/seed_data.py` — generates a sample e-commerce dataset (customers,
  products, orders, order_items) into a local DuckDB file.
- `backend/schema.py` — hardcoded schema description injected into the prompt.
- `backend/query_generator.py` — calls the Claude API with structured
  (tool-use) output to turn a question into `{sql, explanation}`.
- `backend/db.py` — runs the generated SQL against DuckDB, with a minimal
  SELECT-only safety check (full guardrails come in Stage 2).
- `backend/main.py` — FastAPI app exposing `POST /ask`.

## Setup

```bash
cd nl2sql
pip install -r requirements.txt

cd backend
python seed_data.py          # creates analytics.duckdb with sample data

export ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --reload --port 8000
```

## Try it

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What were total sales by product category last year?"}'
```

Response:
```json
{
  "question": "What were total sales by product category last year?",
  "sql": "SELECT ...",
  "explanation": "...",
  "columns": ["category", "revenue"],
  "rows": [{"category": "Electronics", "revenue": 245775.1}, ...]
}
```

## Verified working (no API key needed)

- `seed_data.py` — generates 200 customers, 60 products, 1500 orders, ~3800 order items.
- `db.py` — query execution and the SELECT-only guardrail both tested and passing.

The only piece that needs your `ANTHROPIC_API_KEY` is `query_generator.py`
(the actual NL→SQL step), since that's the one part that calls out to Claude.

## Next stages (not built yet)

- **Stage 2**: real guardrails — read-only DB role, row/time limits, prompt-injection testing.
- **Stage 3**: replace the hardcoded schema with retrieval over table/column
  descriptions (matters once you simulate a schema with 50+ tables).
- **Stage 4**: second LLM call to turn results into a chart spec + insight summary.
- **Stage 5**: eval harness — ~30 test questions with known-correct SQL, scored for accuracy.
- **Stage 6**: conversation memory for follow-up questions.
