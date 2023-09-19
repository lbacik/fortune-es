FROM python:3.11

COPY . /opt/app
WORKDIR /opt/app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ~/.local/bin/poetry config virtualenvs.create false && \
    ~/.local/bin/poetry install --no-dev --no-root --no-interaction --no-ansi

ENV PYTHONPATH=/opt/app
ENV INDEX=fortune

CMD ["sh", "-c", "python -m elastic.app --populate ${INDEX}"]

