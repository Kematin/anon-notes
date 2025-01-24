FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml /app
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY secret.key /app

WORKDIR /app/src

COPY src /app/src/

EXPOSE 8000

CMD ["python", "app.py"]
