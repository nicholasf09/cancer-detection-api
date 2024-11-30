# Gunakan image Python resmi sebagai base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin semua file ke container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (Cloud Run menggunakan port ini)
EXPOSE 8080

# Jalankan aplikasi Flask
CMD ["python", "app.py"]