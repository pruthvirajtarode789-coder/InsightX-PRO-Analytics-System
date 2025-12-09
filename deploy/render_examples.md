# Render deployment quick notes

- Create two web services in Render: `insightx-api` and `insightx-ui`.
- Point `insightx-api` to repo root, start command:
  `uvicorn api.app:app --host 0.0.0.0 --port $PORT`
- Point `insightx-ui` to repo root, start command:
  `streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- Add `API_URL` secret to the Streamlit service to point to the `insightx-api` public URL.

✅ After you paste files

Run pip install -r requirements.txt inside the venv.

Train models: python training/train_models.py

Start API + UI as shown in README.md.

If Streamlit errors about st.secrets not found, either set Streamlit secret or edit app/streamlit_app.py to hard-code API_URL temporarily.                                             add all the thing sin the folder which i have provide to you in the vs code okay
