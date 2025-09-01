FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy app code
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run using Gunicorn (production WSGI server)
# Assuming your Flask app is defined as "app" inside run.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app", "--workers", "3", "--timeout", "90"]
