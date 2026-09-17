from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl

DB = Path(__file__).with_name("snapshots.db")
MAX_BODY_BYTES = 2_000_000
app = FastAPI(title="Website Time Machine", version="0.2.0")

HTML = '''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Website Time Machine</title><style>body{font-family:system-ui;margin:0;background:#0a0d12;color:#eef2f7}main{max-width:900px;margin:50px auto;padding:24px}input,button{padding:14px;border-radius:10px;border:1px solid #28313d;background:#111721;color:#fff}input{width:70%}button{cursor:pointer}section{margin-top:24px;padding:20px;border:1px solid #28313d;border-radius:14px;background:#0f141b}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.muted{color:#8e9aaa}.delta{font-family:ui-monospace,monospace;white-space:pre-wrap}@media(max-width:700px){input{width:calc(100% - 30px)}.grid{grid-template-columns:1fr}}</style></head><body><main><small>WEBSITE TIME MACHINE / MVP</small><h1>See how a website changes.</h1><p class="muted">Capture a public page, then compare its content with an earlier snapshot.</p><form id="f"><input id="u" type="url" placeholder="https://example.com" required><button>Capture</button></form><div id="out"></div></main><script>const f=document.querySelector('#f'),u=document.querySelector('#u'),o=document.querySelector('#out');const e=x=>String(x??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));f.onsubmit=async ev=>{ev.preventDefault();o.innerHTML='<section>Capturing…</section>';try{const r=await fetch('/api/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:u.value})});const d=await r.json();if(!r.ok)throw Error(d.detail||'Capture failed');o.innerHTML=`<section><h2>${e(d.title||'Untitled')}</h2><p class=muted>${e(d.url)}</p><div class=grid><div><b>Snapshot</b><div>${e(d.snapshot_id)}</div></div><div><b>Content hash</b><div>${e(d.content_hash.slice(0,16))}</div></div></div></section>`+(d.previous?`<section><h2>Change report</h2><div class=grid><div>Words: <b>${d.diff.words_added}</b> added / <b>${d.diff.words_removed}</b> removed</div><div>Text similarity: <b>${(d.diff.similarity*100).toFixed(1)}%</b></div></div><p class=delta>${e(d.diff.preview)}</p></section>`:'<section>No previous snapshot yet. Capture this site again later to create the first comparison.</section>')}catch(err){o.innerHTML=`<section>${e(err.message||'Capture failed')}</section>`}};</script></body></html>'''


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS snapshots(id INTEGER PRIMARY KEY, url TEXT NOT NULL, captured_at TEXT NOT NULL, title TEXT, text TEXT NOT NULL, sha256 TEXT NOT NULL)")
    return con


def normalize_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = " ".join(soup.stripped_strings)
    return title, text


def similarity(a: str, b: str) -> float:
    aa, bb = set(a.split()), set(b.split())
    if not aa and not bb:
        return 1.0
    return len(aa & bb) / max(1, len(aa | bb))


class Capture(BaseModel):
    url: HttpUrl


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return HTML


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/capture")
async def capture(payload: Capture) -> dict:
    url = str(payload.url)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password or parsed.port not in (None, 80, 443):
        raise HTTPException(400, "Only ordinary HTTP(S) URLs are supported.")
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(15.0, connect=5.0),
            headers={"User-Agent": "Website-Time-Machine/0.2"},
        ) as client:
            r = await client.get(url)
            r.raise_for_status()
            if len(r.content) > MAX_BODY_BYTES:
                raise HTTPException(413, "Page is larger than the 2 MB capture limit.")
            if "text/html" not in r.headers.get("content-type", "").lower():
                raise HTTPException(415, "The target did not return HTML content.")
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"Could not fetch the page: {exc}") from exc
    title, text = normalize_text(r.text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    with db() as con:
        previous = con.execute("SELECT id,url,captured_at,title,text,sha256 FROM snapshots WHERE url=? ORDER BY id DESC LIMIT 1", (url,)).fetchone()
        cur = con.execute("INSERT INTO snapshots(url,captured_at,title,text,sha256) VALUES(?,?,?,?,?)", (url, datetime.now(timezone.utc).isoformat(), title, text, digest))
        snapshot_id = cur.lastrowid
    result = {"snapshot_id": snapshot_id, "url": url, "title": title, "content_hash": digest, "previous": bool(previous)}
    if previous:
        old_words, new_words = previous[4].split(), text.split()
        old_set, new_set = set(old_words), set(new_words)
        added = [w for w in new_words if w not in old_set][:80]
        removed = [w for w in old_words if w not in new_set][:80]
        result["diff"] = {"words_added": sum(w not in old_set for w in new_words), "words_removed": sum(w not in new_set for w in old_words), "similarity": similarity(previous[4], text), "preview": "ADDED: " + " ".join(added) + "\n\nREMOVED: " + " ".join(removed)}
    return result
