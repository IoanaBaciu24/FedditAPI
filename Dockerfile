FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip \
 && pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY config ./config

RUN poetry install --no-root --only main

RUN poetry run python -c "import nltk; nltk.download('vader_lexicon')"

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
