# Customers API

API REST para registrar y consultar clientes (FastAPI + Pydantic + SQLAlchemy + SQLite).

## Inicio rápido (paso a paso, sin conocimientos previos)

Necesitas una terminal en Linux o macOS. Sigue los pasos en orden.

### Paso 0 — Requisitos

Verifica que tienes Python 3.10 o superior:

```bash
python3 --version
```

En Debian/Ubuntu instala además el soporte de entornos virtuales:

```bash
sudo apt install python3-venv
```

### Paso 1 — Entrar a la carpeta del proyecto

```bash
cd python_fastApi
```

(La carpeta que contiene este README y el archivo `Makefile`.)

### Paso 2 — Instalar (solo la primera vez)

```bash
make install
```

Crea un entorno aislado en `.venv` e instala las dependencias. Tarda 1-2 minutos.

### Paso 3 — Arrancar la API

```bash
make run
```

Este único comando hace **dos cosas**: crea o actualiza la base de datos (`customers.db`) y
arranca el servidor. **No necesitas ejecutar nada más para la base de datos.**

Sabrás que funcionó cuando veas:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Deja esa terminal abierta: la API vive mientras el comando esté corriendo.

### Paso 4 — Probarla

Abre en el navegador: **http://127.0.0.1:8000/docs**. Ahí puedes usar cada endpoint con el
botón "Try it out". También: http://127.0.0.1:8000/health debe mostrar `{"status":"ok"}`.

### Paso 5 — Detenerla

En la terminal donde corre, pulsa `Ctrl + C`.

Para volver a arrancarla otro día solo repites el **Paso 1 y el Paso 3**.

### ¿Qué NO debes hacer?

- No ejecutes `make run` y `uvicorn ...` a la vez: ambos arrancan el servidor y el segundo
  falla con "address already in use". Usa uno solo.
- No hace falta instalar ni configurar ninguna base de datos: SQLite es un archivo.

### Problemas comunes

| Mensaje | Solución |
|---------|----------|
| `make: command not found` | `sudo apt install make`, o usa la sección "Sin make" |
| `ensurepip is not available` | `sudo apt install python3-venv` y repite el Paso 2 |
| `address already in use` | Ya hay una API corriendo; ciérrala con `Ctrl + C` o usa otro puerto |
| `python: command not found` | Usa `python3` (en Linux `python` suele no existir) |

## Sin make (alternativa manual)

Equivale a los pasos 2 y 3. Ejecuta línea por línea dentro de la carpeta del proyecto:

```bash
python3 -m venv .venv              # crea el entorno aislado
source .venv/bin/activate          # actívalo (el prompt mostrará "(.venv)"); Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
alembic upgrade head               # crea/actualiza la base de datos
uvicorn app.main:app --reload      # arranca la API
```

Cada vez que abras una terminal nueva debes repetir `source .venv/bin/activate` antes de
`uvicorn`. Importante: confirma que ves `(.venv)` antes de `pip install`; si no, instalarías
en tu Python global.

## Ejecución con Docker (alternativa)

```bash
docker compose up --build
```

La API queda en http://127.0.0.1:8000. Las migraciones se aplican al arrancar y la base
persiste en un volumen. No necesitas Python instalado.

## Tests

(Requieren haber hecho antes `make install`.)

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
