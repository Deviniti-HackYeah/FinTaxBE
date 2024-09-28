FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.7.1  \
    && poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-root

COPY . .
RUN poetry install

CMD ["./scripts/run_prod.sh"]
