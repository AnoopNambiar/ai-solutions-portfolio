FROM python:3.13-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY index.html .

EXPOSE 5000

CMD ["python", "app.py"]