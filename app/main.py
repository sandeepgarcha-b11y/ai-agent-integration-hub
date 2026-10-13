"""CX Agent Integration Hub: the web server and its endpoints."""
import logging
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.db import connect, init_db

log = logging.getLogger("hub")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # create tables on startup if they don't exist yet
    yield


app = FastAPI(title="CX Agent Integration Hub", lifespan=lifespan)


@app.get("/ping")
def ping():
    """Liveness: is the process up? Deliberately checks nothing else."""
    return {"status": "alive"}


@app.get("/health")
def health():
    """Readiness: can we do our job right now? That needs the database."""
    try:
        with connect() as conn:
            conn.execute("SELECT 1").fetchone()
    except sqlite3.Error:
        log.exception("health check: database unreachable")  # details stay in our logs
        return JSONResponse(status_code=503, content={"status": "unavailable"})
    return {"status": "ok"}


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """Look up one order. Shows the difference between 'not found' and 'broken'."""
    with connect() as conn:
        row = conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="order not found")
    return dict(row)
