# URL Shortener API

A URL shortening service built with Python and FastAPI. Paste a long URL and get a short shareable link back instantly.

## Features

- Shorten any URL to a 6-character code
- Automatic redirect when visiting the short link
- Click tracking - see how many times a link was visited
- Clean web interface
- REST API with auto-generated docs

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Getting Started

**1 — Clone the repo**
```bash
git clone https://github.com/sujndoes/url-shortener.git
cd url-shortener
```

**2 — Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3 — Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy
```

**4 — Run the server**
```bash
uvicorn main:app --reload
```

**5 — Open in browser**