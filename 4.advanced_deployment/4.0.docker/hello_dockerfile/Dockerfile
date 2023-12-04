FROM python:3.11-slim
RUN pip install fastapi uvicorn
COPY app.py .
CMD uvicorn app:app --host 0.0.0.0 