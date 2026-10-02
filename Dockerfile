FROM python:3.13-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
        urllib3 \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY index.html .

EXPOSE 5000

CMD ["python", "app.py"]