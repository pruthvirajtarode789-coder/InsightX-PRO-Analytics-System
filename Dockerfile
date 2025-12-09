FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
# default: run API. For UI use a different container or change cmd
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
