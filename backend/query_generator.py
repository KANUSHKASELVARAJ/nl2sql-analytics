"""
Stage 1: turns a natural-language question into SQL using Claude's
structured output (tool use), constrained to a fixed JSON schema.
"""
import os
import anthropic
from schema import SCHEMA_DESCRIPTION

MODEL = "claude-sonnet-5"

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = f"""You are a SQL generation assistant for a DuckDB analytics database.
Given a user's natural language question, generate a single read-only SQL query
that answers it, using ONLY the tables and columns described below.

{SCHEMA_DESCRIPTION}

Rules:
- Only generate SELECT statements. Never generate INSERT, UPDATE, DELETE, DROP,
  ALTER, CREATE, or any other statement that modifies data or schema.
- Only reference tables/columns that exist in the schema above.
- If the question cannot be answered with the available schema, set "sql" to
  an empty string and explain why in "explanation".
- Always call the `generate_sql` tool with your result — do not respond in plain text.
"""

SQL_TOOL = {
    "name": "generate_sql",
    "description": "Return the generated SQL query and a short explanation of what it does.",
    "input_schema": {
        "type": "object",
        "properties": {
            "sql": {
                "type": "string",
                "description": "The SQL SELECT query that answers the question, or empty string if impossible.",
            },
            "explanation": {
                "type": "string",
                "description": "A short (1-2 sentence) explanation of what the query does, or why it can't be answered.",
            },
        },
        "required": ["sql", "explanation"],
    },
}


def generate_sql(question: str) -> dict:
    """Calls Claude to turn `question` into a SQL query + explanation."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        tools=[SQL_TOOL],
        tool_choice={"type": "tool", "name": "generate_sql"},
        messages=[{"role": "user", "content": question}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "generate_sql":
            return {
                "sql": block.input.get("sql", ""),
                "explanation": block.input.get("explanation", ""),
            }

    # Shouldn't happen since tool_choice forces the tool, but just in case
    return {"sql": "", "explanation": "Model did not return a structured result."}
