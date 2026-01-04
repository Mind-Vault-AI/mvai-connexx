FROM python:3.9-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create user
RUN groupadd -r mvai && useradd -r -g mvai mvai_user

# Copy application code
COPY . .

# Fix permissions
RUN chown -R mvai_user:mvai /app

# Switch to non-root user
USER mvai_user

EXPOSE 5000

# Start app directly with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]

