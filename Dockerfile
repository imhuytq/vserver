FROM python:3.10

WORKDIR /app

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -

ENV PATH="${PATH}:/opt/poetry/bin"

RUN poetry config virtualenvs.create false

COPY ./vserver/pyproject.toml ./vserver/poetry.lock /app/

RUN poetry install --no-root --only main

COPY ./vserver /app

CMD ["bash", "/app/bin/start.sh"]
