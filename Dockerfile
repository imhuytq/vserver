FROM python:3.10

WORKDIR /app

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -

ENV PATH="${PATH}:/opt/poetry/bin"

RUN poetry config virtualenvs.create false

COPY ./vserver/pyproject.toml ./vserver/poetry.lock /app/

RUN poetry install --no-root --only main

COPY ./vserver /app

CMD ["uvicorn", "vserver.main:app", "--host", "0.0.0.0", "--port", "8080"]
