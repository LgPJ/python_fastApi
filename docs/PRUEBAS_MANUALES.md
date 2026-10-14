# Pruebas manuales

Equivalen a lo que automatizan `make test` (pytest) y `make smoke` (`scripts/smoke_test.sh`).

## Automatizadas

```bash
make install   # una sola vez
make check     # pytest + smoke end-to-end
```

## Preparar entorno manual

```bash
make migrate && make run        # API en http://127.0.0.1:8000
```

Para empezar de cero: detener el servidor, `rm customers.db`, `make migrate && make run`.
Alternativa gráfica: abrir http://127.0.0.1:8000/docs y usar "Try it out".

Los pasos son secuenciales (el primer cliente creado tiene `id = 1`).

## Casos

| # | Caso | Comando | Esperado |
|---|------|---------|----------|
| 1 | Health | `curl -i localhost:8000/health` | 200 `{"status":"ok"}` |
| 2 | Crear cliente | `curl -i -X POST localhost:8000/customers -H 'Content-Type: application/json' -d '{"name":"Juan Pérez","email":"juan@example.com"}'` | 201, `status":"PENDING"`, `id":1`, `created_at` presente |
| 3 | Email duplicado | mismo comando con `"email":"JUAN@example.com"` | 409 `already exists` |
| 4 | Email inválido | `-d '{"name":"X","email":"no-es-email"}'` | 422 |
| 5 | Nombre vacío | `-d '{"name":"  ","email":"a@example.com"}'` | 422 |
| 6 | Falta campo | `-d '{"name":"X"}'` | 422 |
| 7 | Obtener existente | `curl -i localhost:8000/customers/1` | 200, mismo cliente |
| 8 | Obtener inexistente | `curl -i localhost:8000/customers/999` | 404 `Customer 999 not found` |
| 9 | Id no numérico | `curl -i localhost:8000/customers/abc` | 422 |
| 10 | Cambiar a ACTIVE | `curl -i -X PATCH localhost:8000/customers/1/status -H 'Content-Type: application/json' -d '{"status":"ACTIVE"}'` | 200, `status":"ACTIVE"` |
| 11 | Status inválido | `-d '{"status":"DELETED"}'` (mismo PATCH) | 422 |
| 12 | Status en minúscula | `-d '{"status":"active"}'` | 422 (el enum es sensible a mayúsculas) |
| 13 | PATCH cliente inexistente | `curl -i -X PATCH localhost:8000/customers/999/status -H 'Content-Type: application/json' -d '{"status":"ACTIVE"}'` | 404 |
| 14 | Listar todos | `curl -i localhost:8000/customers` | 200, arreglo con el cliente |
| 15 | Filtro con resultados | `curl -i 'localhost:8000/customers?status=ACTIVE'` | 200, contiene a Juan |
| 16 | Filtro sin resultados | `curl -i 'localhost:8000/customers?status=BLOCKED'` | 200 `[]` |
| 17 | Filtro inválido | `curl -i 'localhost:8000/customers?status=NOPE'` | 422 |
| 18 | Paginación | crear 3 clientes (`ana`, `beto`, `carla`) y `curl -i 'localhost:8000/customers?limit=2&offset=1'` | 200, 2 clientes (los de posiciones 2 y 3), header `x-total-count: <total>` |
| 19 | Offset más allá del final | `curl -i 'localhost:8000/customers?offset=1000'` | 200 `[]`, `x-total-count` sigue siendo el total |
| 20 | Total respeta filtro | `curl -i 'localhost:8000/customers?status=ACTIVE&limit=1'` | `x-total-count` = cantidad de ACTIVE |
| 21 | Paginación inválida | `?limit=0`, `?limit=101`, `?offset=-1`, `?limit=x` | 422 en todos |
| 22 | Persistencia | detener y reiniciar el servidor, repetir caso 7 | 200 (datos persisten en `customers.db`) |

## Verificar la base directamente (opcional)

```bash
sqlite3 customers.db 'select id, name, email, status, created_at from customers;'
```
