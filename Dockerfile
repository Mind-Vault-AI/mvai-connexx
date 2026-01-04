FROM python:3.9-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create user
RUN groupadd -r mvai && useradd -r -g mvai mvai_user

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Fix permissions
RUN chown -R mvai_user:mvai /app

# Switch to non-root user
USER mvai_user

# Environment variables voor Fly.io deployment
ENV DATABASE_PATH=/app/data/mvai_connexx.db
ENV PORT=5000

EXPOSE 5000

# Use startup script (handles volume mount setup)
CMD ["./start.sh"]
