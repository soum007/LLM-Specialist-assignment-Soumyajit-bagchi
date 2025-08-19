FROM python:3.11-slim

WORKDIR /app

# System deps for pdfplumber (Pillow + dependencies)
RUN apt-get update && apt-get install -y     build-essential     libjpeg-dev     zlib1g-dev     poppler-utils     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
