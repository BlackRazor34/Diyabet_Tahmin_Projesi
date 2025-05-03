FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY diabetes_rf_model.pkl /app/
COPY scaler.pkl /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
EXPOSE 8000 

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]