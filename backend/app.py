from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from prometheus_client import Counter, generate_latest
from starlette.responses import Response

from influx_client_helper import InfluxManager

app = FastAPI()
db = InfluxManager()

REQUEST_COUNT = Counter("requests_total", "Total Requests")

class Telemetry(BaseModel):
    machine_id: str
    temperature: float
    latency: float
    error_count: int
    timestamp: int

@app.get("/health")
def health():
    return {"status": "ok", "time": str(datetime.utcnow())}

@app.post("/ingest")
def ingest(data: Telemetry):
    REQUEST_COUNT.inc()
    db.write_metric(data.dict())
    return {"status": "ingested"}

@app.get("/prometheus")
def metrics():
    return Response(generate_latest(), media_type = "text/plain")
 
