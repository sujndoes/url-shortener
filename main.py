from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import URL
import random
import string

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 80px auto; padding: 20px; background: #f5f5f5; }
            h1 { color: #333; }
            input[type="text"] { width: 100%; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; margin: 10px 0; box-sizing: border-box; }
            button { background: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; width: 100%; }
            button:hover { background: #45a049; }
            #result { margin-top: 20px; padding: 16px; background: white; border-radius: 6px; display: none; }
            a { color: #4CAF50; word-break: break-all; }
        </style>
    </head>
    <body>
        <h1>URL Shortener</h1>
        <p>Paste a long URL below to get a short one.</p>
        <input type="text" id="urlInput" placeholder="https://example.com" />
        <button onclick="shortenURL()">Shorten</button>
        <div id="result">
            <p>Your short URL:</p>
            <a id="shortLink" href="#" target="_blank"></a>
        </div>
        <script>
            async function shortenURL() {
                const url = document.getElementById('urlInput').value;
                if (!url) return alert('Please enter a URL');
                const response = await fetch('/shorten?original_url=' + encodeURIComponent(url), { method: 'POST' });
                const data = await response.json();
                const resultDiv = document.getElementById('result');
                const shortLink = document.getElementById('shortLink');
                shortLink.href = data.short_url;
                shortLink.textContent = data.short_url;
                resultDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def shorten_url(original_url: str, db: Session = Depends(get_db)):
    code = generate_code()
    new_url = URL(original_url=original_url, short_code=code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_code": code, "short_url": f"http://localhost:8000/{code}"}

@app.get("/stats/{code}")
def get_stats(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks
    }

@app.get("/{code}")
def redirect_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url.clicks += 1
    db.commit()
    return RedirectResponse(url.original_url)