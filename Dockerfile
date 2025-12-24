FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd -r mvai && useradd -r -g mvai mvai_user
COPY . .
RUN chown -R mvai_user:mvai /app
USER mvai_user
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
