# Customers API

API REST para registrar y consultar clientes (FastAPI + Pydantic + SQLAlchemy + SQLite).

## Requisitos

- Python 3.10+ (o Docker)

## Ejecución local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head            # crea customers.db con el esquema
uvicorn app.main:app --reload
```

Documentación interactiva: http://localhost:8000/docs

## Ejecución con Docker

```bash
docker compose up --build
```

La base SQLite persiste en un volumen. Las migraciones se aplican al arrancar.

## Tests

```bash
make test     # pytest (BD en memoria)
make smoke    # end-to-end con servidor real y BD temporal (curl)
make check    # ambos
```

Pruebas paso a paso a mano: [docs/PRUEBAS_MANUALES.md](docs/PRUEBAS_MANUALES.md).

## Endpoints

| Método | Ruta                              | Descripción                              | Códigos            |
|--------|-----------------------------------|------------------------------------------|--------------------|
| POST   | `/customers`                      | Crea cliente (status inicial `PENDING`)  | 201, 409, 422      |
| GET    | `/customers?status=&limit=&offset=` | Lista paginada, filtro opcional. Total en header `X-Total-Count` | 200, 422 |
| GET    | `/customers/{customer_id}`        | Obtiene un cliente                       | 200, 404, 422      |
| PATCH  | `/customers/{customer_id}/status` | Cambia el status                         | 200, 404, 422      |
| GET    | `/health`                         | Health check                             | 200                |

Estados válidos: `ACTIVE`, `PENDING`, `BLOCKED`.

## Ejemplos

```bash
# Crear
curl -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Pérez", "email": "juan@example.com"}'

# Email duplicado -> 409
curl -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "Otro", "email": "juan@example.com"}'

# Listar (filtro + paginación; limit 1-100, default 50; offset >= 0)
curl -i "http://localhost:8000/customers?status=ACTIVE&limit=10&offset=0"

# Obtener
curl http://localhost:8000/customers/1

# Actualizar status
curl -X PATCH http://localhost:8000/customers/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "ACTIVE"}'

# Health
curl http://localhost:8000/health
```

## Configuración

| Variable       | Default                     |
|----------------|-----------------------------|
| `DATABASE_URL` | `sqlite:///./customers.db`  |

## Estructura

```
app/
  api/            # capa HTTP: routers, dependencias, mapeo error -> HTTP
  services/       # reglas de negocio
  repositories/   # acceso a datos (SQLAlchemy)
  models/         # modelos ORM
  schemas/        # modelos Pydantic (request/response)
  core/           # config, DB, excepciones de dominio
alembic/          # migraciones
tests/
```

Detalle de diseño y decisiones: ver [EXPLICACION.md](EXPLICACION.md).
