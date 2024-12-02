# Gunakan image Python versi 3.10 yang ringan
FROM python:3.10-slim

# Set variabel lingkungan untuk unbuffered logs
ENV PYTHONUNBUFFERED=True
ENV PORT=8080  # Port default untuk Cloud Run

# Set direktori kerja aplikasi
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Install dependencies sistem untuk Pillow dan TensorFlow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Salin semua file dari folder lokal ke dalam container
COPY . .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Menjalankan aplikasi Flask menggunakan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
