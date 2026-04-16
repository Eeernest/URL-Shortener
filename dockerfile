FROM python:3.14.2

WORKDIR /app

COPY pyproject.toml readme.md ./

COPY app/ ./app

RUN python -m pip install --no-cache-dir .

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]