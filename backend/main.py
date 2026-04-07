import json
import os
import shutil
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import OverallStats, DeptStat, CompanyStat, TimelineStat, CTCBucket, Student
from parser import parse_excel
from analytics import (
    get_overall_stats, get_dept_stats, get_company_stats,
    get_timeline_stats, get_ctc_distribution, get_role_stats
)
from database import init_db, fetch_all_students, fetch_students_filtered
from watcher import start_watcher

# ── Config ────────────────────────────────────────────────────────────────────
with open("config.json") as f:
    CONFIG = json.load(f)

EXCEL_PATH     = CONFIG["excel_filename"]
UPLOAD_PASSWORD = CONFIG["upload_password"]


# ── WebSocket Manager ─────────────────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: str):
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)


manager = ConnectionManager()


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Init DB (create/migrate table)
    init_db()
    Path("data").mkdir(exist_ok=True)

    # 2. Parse Excel on startup
    if Path(EXCEL_PATH).exists():
        records = parse_excel(EXCEL_PATH)
        print(f"[Startup] Loaded {len(records)} students")
    else:
        print(f"[Startup] WARNING: Excel not found at '{EXCEL_PATH}'")

    # 3. Store event loop for thread-safe WS broadcast
    loop = asyncio.get_event_loop()
    app.state.loop = loop

    # 4. File watcher callback
    def on_excel_change():
        parse_excel(EXCEL_PATH)
        asyncio.run_coroutine_threadsafe(
            manager.broadcast('{"event":"DATA_UPDATED"}'),
            app.state.loop
        )

    observer = start_watcher(EXCEL_PATH, on_excel_change)

    yield  # ← app runs here

    observer.stop()


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="DTU M.Tech Placements API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── REST Endpoints ────────────────────────────────────────────────────────────
@app.get("/api/stats")
def overall_stats():
    try:
        return get_overall_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/departments", response_model=List[DeptStat])
def dept_stats():
    try:
        return get_dept_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/companies", response_model=List[CompanyStat])
def company_stats():
    try:
        return get_company_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/timeline", response_model=List[TimelineStat])
def timeline():
    try:
        return get_timeline_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ctc-distribution", response_model=List[CTCBucket])
def ctc_dist():
    try:
        return get_ctc_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/roles")
def get_roles():
    try:
        return get_role_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/students", response_model=List[Student])
def students(
    department: Optional[str] = None,
    company: Optional[str] = None,
    min_ctc: Optional[float] = None,
    max_ctc: Optional[float] = None,
):
    try:
        return fetch_students_filtered(department, company, min_ctc, max_ctc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_excel(
    file: UploadFile = File(...),
    password: str = Form(...),
):
    if password != UPLOAD_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx / .xls files allowed")

    Path("data").mkdir(exist_ok=True)
    with open(EXCEL_PATH, "wb") as f:
        shutil.copyfileobj(file.file, f)

    records = parse_excel(EXCEL_PATH)
    await manager.broadcast('{"event":"DATA_UPDATED"}')
    return {"message": f"Uploaded successfully. {len(records)} students loaded."}


@app.get("/api/health")
def health():
    from database import get_connection
    try:
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        conn.close()
        return {
            "status": "ok",
            "excel_exists": Path(EXCEL_PATH).exists(),
            "students_in_db": count,    # ← tells you instantly if DB is empty
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# ── WebSocket ──────────────────────────────────────────────────────────────────
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)