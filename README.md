# transport-hub-server

A FastAPI backend for the UoS Sustainable Travel Hub — serves transport data, user auth, favourites, and sustainability tracking.

## Requirements

- Python 3.11+
- pip

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/UoS-Sustainability/transport-hub-server.git
cd transport-hub-server
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```
DATABASE_URL=postgresql://user:password@localhost:5432/transport_hub
SECRET_KEY=your-secret-key-here
```

> For local development without PostgreSQL, the default SQLite database (`dev.db`) will be used automatically if `DATABASE_URL` is not set.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`.

## API Docs

Once running, FastAPI auto-generates interactive docs:

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |
| `http://localhost:8000/health` | Health check |
