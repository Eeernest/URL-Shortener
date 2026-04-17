FROM python:3.12-slim

WORKDIR /code

COPY pyproject.toml ./

COPY app/ ./app/

RUN python -m pip install --no-cache-dir .

COPY . .

ENV PYTHONPATH=/code

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]