FROM python:3.12-slim

RUN useradd --create-home appuser
WORKDIR /home/appuser/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_secure.py spam_model.joblib ./
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app_secure:app", "--host", "0.0.0.0", "--port", "8000"]
