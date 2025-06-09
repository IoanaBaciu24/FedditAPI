FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NLTK_DATA=/usr/share/nltk_data

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
 && pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY config ./config

RUN echo "Installing dependencies..." \
 && poetry install --no-root --without dev \
 && echo "Dependencies installed"

RUN echo "Downloading NLTK data..." \
 && poetry run python -c "import nltk; nltk.download('vader_lexicon')" \
 && echo "NLTK data downloaded"

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
