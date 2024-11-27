FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY app/ app/

CMD ["streamlit", "run", "app/app.py", "--server.port", "80"]
