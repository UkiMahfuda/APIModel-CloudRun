# Gunakan image Python versi 3.10 yang ringan
FROM python:3.10-slim

# Set variabel lingkungan untuk unbuffered logs
ENV PYTHONUNBUFFERED True

# Set direktori kerja aplikasi
ENV APP_HOME /app
WORKDIR $APP_HOME

# Salin semua file dari folder lokal ke dalam container
COPY . ./

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Menjalankan aplikasi Flask menggunakan Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
