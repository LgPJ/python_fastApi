#!/usr/bin/env bash
# End-to-end smoke test: starts the API on a throwaway SQLite DB and exercises every endpoint with curl.
# Usage: scripts/smoke_test.sh [port]     (run from the repo root)
set -uo pipefail

PORT="${1:-8765}"
BASE="http://127.0.0.1:${PORT}"
PY="${PYTHON:-.venv/bin/python}"
TMP_DB="$(mktemp -u /tmp/customers-smoke-XXXXXX.db)"
export DATABASE_URL="sqlite:///${TMP_DB}"

PASS=0; FAIL=0
BODY=""; CODE=""

cleanup() {
  [[ -n "${SERVER_PID:-}" ]] && kill "$SERVER_PID" 2>/dev/null
  rm -f "$TMP_DB"
}
trap cleanup EXIT

request() { # method path [json]
  local out
  if [[ $# -ge 3 ]]; then
    out=$(curl -s -w $'\n%{http_code}' -X "$1" "${BASE}$2" -H 'Content-Type: application/json' -d "$3")
  else
    out=$(curl -s -w $'\n%{http_code}' -X "$1" "${BASE}$2")
  fi
  CODE="${out##*$'\n'}"
  BODY="${out%$'\n'*}"
}

check() { # description expected_code [expected_body_substring]
  if [[ "$CODE" == "$2" && ( -z "${3:-}" || "$BODY" == *"$3"* ) ]]; then
    echo "  PASS  $1"; PASS=$((PASS + 1))
  else
    echo "  FAIL  $1 (got $CODE: $BODY; expected $2 ${3:-})"; FAIL=$((FAIL + 1))
  fi
}

echo "Applying migrations on $TMP_DB"
"$PY" -m alembic upgrade head >/dev/null 2>&1 || { echo "migration failed"; exit 1; }

echo "Starting API on port $PORT"
"$PY" -m uvicorn app.main:app --port "$PORT" --log-level warning &
SERVER_PID=$!
for _ in $(seq 1 30); do
  curl -s "${BASE}/health" >/dev/null 2>&1 && break
  sleep 0.2
done

echo "Running checks"
request GET /health;                                                        check "health ok" 200 '"status":"ok"'
request POST /customers '{"name":"Juan Pérez","email":"juan@example.com"}'; check "create customer" 201 '"status":"PENDING"'
request POST /customers '{"name":"Otro","email":"JUAN@example.com"}';       check "duplicate email (case-insensitive)" 409
request POST /customers '{"name":"X","email":"no-es-email"}';               check "invalid email" 422
request POST /customers '{"name":"  ","email":"a@example.com"}';            check "blank name" 422
request GET /customers/1;                                                   check "get existing" 200 '"id":1'
request GET /customers/999;                                                 check "get missing" 404
request GET /customers/abc;                                                 check "get non-numeric id" 422
request PATCH /customers/1/status '{"status":"ACTIVE"}';                    check "patch to ACTIVE" 200 '"status":"ACTIVE"'
request PATCH /customers/1/status '{"status":"DELETED"}';                   check "patch invalid status" 422
request PATCH /customers/999/status '{"status":"ACTIVE"}';                  check "patch missing customer" 404
request GET '/customers?status=ACTIVE';                                     check "list filter ACTIVE" 200 'juan@example.com'
request GET '/customers?status=BLOCKED';                                    check "list filter BLOCKED is empty" 200 '[]'
request GET '/customers?status=NOPE';                                       check "list invalid status" 422
request GET /customers;                                                     check "list all" 200 'juan@example.com'

echo
echo "Result: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
