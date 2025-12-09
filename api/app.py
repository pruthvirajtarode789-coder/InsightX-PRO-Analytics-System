# api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd, numpy as np, os, joblib
from datetime import timedelta
from typing import Optional

app = FastAPI(title="InsightX PRO API")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

def load_sales():
    path = os.path.join(DATA_DIR, "sales_sample.csv")
    return pd.read_csv(path, parse_dates=["date"])

@app.get("/")
def root():
    return {"status":"InsightX PRO API running ✅"}

@app.get("/health")
def health():
    return {"status":"ok"}

class ForecastRequest(BaseModel):
    product_id: Optional[str] = None
    days: int = 30

@app.post("/forecast")
def forecast(req: ForecastRequest):
    df = load_sales()
    if req.product_id:
        df = df[df["product_id"]==req.product_id]
    ts = df.groupby("date")["revenue"].sum().reset_index().set_index("date").resample("D").sum().fillna(0)
    window = 14
    ts["ma"] = ts["revenue"].rolling(window=window, min_periods=1).mean()
    last = float(ts["ma"].iloc[-1]) if not ts["ma"].empty else 0.0
    fc = []
    start = ts.index.max() + timedelta(days=1) if not ts.empty else pd.to_datetime("today").normalize()
    for i in range(req.days):
        val = float(max(0, last * (1 + np.random.normal(0,0.06))))
        fc.append({"date": (start + timedelta(days=i)).strftime("%Y-%m-%d"), "forecast": round(val,2)})
    return {"product_id": req.product_id, "forecast": fc}

class SegmentRequest(BaseModel):
    n_clusters: int = 4

@app.post("/segment")
def segment(req: SegmentRequest):
    path = os.path.join(DATA_DIR, "customers_sample.csv")
    df = pd.read_csv(path)
    from sklearn.cluster import KMeans
    X = df[["total_orders","avg_order_value","tenure_days"]].fillna(0)
    km = KMeans(n_clusters=req.n_clusters, random_state=42).fit(X)
    df["segment"] = km.labels_
    counts = df["segment"].value_counts().sort_index().to_dict()
    return {"n_clusters": req.n_clusters, "counts": counts, "sample": df.head(10).to_dict(orient="records")}

class AnomRequest(BaseModel):
    threshold: float = 2.0

@app.post("/anomaly")
def anomaly(req: AnomRequest):
    df = load_sales()
    ts = df.groupby("date")["revenue"].sum().reset_index()
    mean = ts["revenue"].mean()
    std = ts["revenue"].std()
    anomalies = ts[(ts["revenue"] > mean + req.threshold*std) | (ts["revenue"] < mean - req.threshold*std)]
    return {"mean": round(mean,2), "std": round(std,2), "anomalies": anomalies.to_dict(orient="records")}
