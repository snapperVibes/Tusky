FROM python:3.9

WORKDIR /src
COPY ./pyproject.toml ./poetry.lock* /src/
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY . /src
EXPOSE 8000
RUN poetry install --no-root --no-dev
CMD ["uvicorn", "__init__:app", "--reload", "--host", "0.0.0.0" ]
