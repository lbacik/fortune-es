FROM python:3.11

COPY . /opt/app
WORKDIR /opt/app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ~/.local/bin/poetry config virtualenvs.create false && \
    ~/.local/bin/poetry install --no-dev --no-interaction --no-ansi

ENV FORTUNE_API="https://api.fortune.luka.sh"
ENV INDEX="fortune"

ENTRYPOINT ["fes"]
