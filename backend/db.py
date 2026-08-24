"""
Stage 1: basic query execution against DuckDB.
Full guardrails (read-only DB role, row limits, injection testing) land in Stage 2 —
this is just a minimal sanity check so Stage 1 isn't wide open.
"""
import re
import duckdb

DB_PATH = "analytics.duckdb"

# Very basic Stage-1 check: only allow queries that start with SELECT and
# don't contain obvious mutating keywords. This is NOT a real guardrail yet.
FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|ATTACH|COPY|PRAGMA)\b",
    re.IGNORECASE,
)


class UnsafeQueryError(Exception):
    pass


def validate_select_only(sql: str) -> None:
    stripped = sql.strip().rstrip(";")
    if not stripped:
        raise UnsafeQueryError("Empty query.")
    if not stripped.upper().startswith("SELECT"):
        raise UnsafeQueryError("Only SELECT queries are allowed.")
    if FORBIDDEN_KEYWORDS.search(stripped):
        raise UnsafeQueryError("Query contains a forbidden keyword.")


def run_query(sql: str, row_limit: int = 500):
    validate_select_only(sql)
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        result = con.execute(sql).fetchmany(row_limit)
        columns = [desc[0] for desc in con.description]
        rows = [dict(zip(columns, row)) for row in result]
        return {"columns": columns, "rows": rows}
    finally:
        con.close()
