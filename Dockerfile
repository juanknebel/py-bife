FROM python:3.11.6
LABEL authors="Juan"

RUN apt-get update && apt-get install -y curl sqlite3

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV APP_HOME="/code"
ENV PATH="/root/.local/bin":${PATH}

RUN mkdir -p $APP_HOME
RUN mkdir -p "$APP_HOME/database"
RUN mkdir -p "$APP_HOME/migrations"

WORKDIR "$APP_HOME"
COPY poetry.lock .
COPY pyproject.toml .
COPY README.md .
COPY run.py .
COPY py_bife "/code/py_bife"
COPY .env.prod .
COPY sqlite-db/prod.db "/code/database"

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV APP_ENVIRONMENT=production
ENV HOST=localhost
ENV PORT 13000
ENV WORKERS=8

WORKDIR "$APP_HOME"
EXPOSE $PORT
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "13000", "--workers", "8"]
