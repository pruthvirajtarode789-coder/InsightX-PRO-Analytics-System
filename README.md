# InsightX PRO — Enterprise Business Analytics & Forecasting

**Overview**
InsightX PRO is a client-ready, production-oriented demo showing:
- Time-series forecasting (moving-average placeholder)
- Customer segmentation (KMeans)
- Revenue anomaly detection
- FastAPI backend with endpoints for forecast/segment/anomaly
- Streamlit UI that calls backend endpoints
- Training pipeline to produce saved models (joblib)
- Realistic sample datasets
- Deployment config for Render (render.yaml) and Dockerfile

---

## Quick start (local)

1. Unpack project into a folder, e.g.
   `C:\Users\pruth\OneDrive\Desktop\InsightX_PRO_FULL`

2. Create & activate virtual environment:
- Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate


macOS / Linux:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


(Optional) Train models:

python training/train_models.py


This creates models/segmentation.joblib

Start API (terminal 1):

uvicorn api.app:app --reload --host 127.0.0.1 --port 8000


Start Streamlit UI (terminal 2):

streamlit run app/streamlit_app.py --server.port 8501 --server.address 127.0.0.1


Open:

UI: http://localhost:8501

API: http://127.0.0.1:8000/health

Deploy

Use the provided render.yaml or follow the deploy/render_examples.md

For Streamlit Cloud, add API_URL secret to point to your API endpoint.

Project Structure

(see file tree)

Contact

Project generated for client demos and portfolio delivery.


---
