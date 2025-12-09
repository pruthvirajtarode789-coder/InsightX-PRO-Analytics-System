# InsightX PRO — Project Report (Client-ready)

## 1. Executive Summary
InsightX PRO is an enterprise-ready analytics demo that demonstrates forecasting, segmentation, and anomaly detection. Built with Python (FastAPI, Streamlit) it allows business users to generate forecasts, segment customers and surface revenue anomalies.

## 2. Objectives
- Provide actionable forecasting for product revenue
- Segment customers into meaningful groups
- Detect revenue anomalies for alerts

## 3. Architecture
- Presentation: Streamlit UI
- API: FastAPI endpoints for inference
- ML: scikit-learn models (KMeans) and time-series heuristics
- Data: CSV-driven sample dataset for offline demos

(See `docs/diagrams_instructions.md` for how to generate actual diagrams in images)

## 4. Data
- `data/sales_sample.csv`: daily revenue per product
- `data/customers_sample.csv`: customer statistics
- `data/transactions_sample.csv`: user transactions sample

## 5. ML & Methods
- Forecast: 14-day moving average baseline with stochastic perturbation (placeholder for ARIMA/Prophet)
- Segmentation: KMeans clustering on [total_orders, avg_order_value, tenure_days]
- Anomaly Detection: Z-score thresholding on daily revenue

## 6. API Endpoints
- `GET /` — Health
- `GET /health` — Health check
- `POST /forecast` — body: { product_id?, days } -> forecast list
- `POST /segment` — body: { n_clusters } -> cluster counts + sample
- `POST /anomaly` — body: { threshold } -> anomalies list

## 7. Deployment
- Render example `render.yaml` included
- Dockerfile included for containerized deployment

## 8. Next steps / Enhancements (for client)
- Replace moving-average with Prophet or SARIMA models
- Persist datasets in PostgreSQL / S3 and add authentication
- Add alerting (Slack, email) for anomalies
- Add model monitoring and metrics (Prometheus/Grafana)
