# Atlasy backend

FastAPI service with a public health check and a JWT-protected `/me` route that verifies **Supabase Auth** access tokens.

## Prerequisites

- Python 3.11+ recommended (3.12+ supported)
- macOS with zsh (activation commands below)

## Virtual environment

Create is optional if `.venv` already exists.

```bash
cd ~/atlasy_backend
python3 -m venv .venv
```

Activate **zsh** (macOS):

```bash
source .venv/bin/activate
```

Deactivate when finished:

```bash
deactivate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Copy the environment template and edit values:

```bash
cp .env.example .env
```

### Required variables

| Variable | Description |
|----------|-------------|
| `SUPABASE_JWT_SECRET` | In Supabase: **Project Settings → API → JWT Secret**. Used to verify HS256 user access tokens (same signing secret Supabase uses). Do **not** commit this value. |

### Optional variables

| Variable | Description |
|----------|-------------|
| `SUPABASE_JWT_ISSUER` | If set, the `iss` claim must match (e.g. `https://<project-ref>.supabase.co/auth/v1`). |
| `CORS_ORIGINS` | Comma-separated browser/Expo origins allowed by CORS (default includes common Expo dev ports). Add your machine’s LAN URL when testing on a device (e.g. `http://192.168.1.10:8081`). |

### Auth strategy

This API verifies tokens with **`SUPABASE_JWT_SECRET`** (symmetric HS256). This matches Supabase’s documented approach for backend JWT validation and avoids fetching JWKS.

**Do not** put the Supabase **service role** key in the client or in committed files; if you add server-side admin operations later, keep that key only in secure server environment variables.

## Run locally

From the project root with `.env` present and venv activated:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Call `/me` with header:

```http
Authorization: Bearer <supabase_user_access_token>
```

Use the access token from your Supabase-authenticated client session (not the anon or service role keys).
