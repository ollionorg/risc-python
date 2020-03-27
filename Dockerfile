FROM python:3.8-slim

WORKDIR /app

RUN apt-get -qq update && \
    apt-get -qq install make

COPY . /app

RUN pip install --upgrade pip wheel setuptools poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

ARG BUILD_DATETIME
ARG SHA1
ARG VERSION

LABEL io.github.2ndWatch.description="RISC CLI and API client module" \
    io.github.2ndWatch.documentation="https://2ndWatch.github.io/risc-python/" \
    io.github.2ndWatch.image.revision=$SHA1 \
    io.github.2ndWatch.image.version=$VERSION \
    io.github.2ndWatch.image.vendor="2ndWatch" \
    io.github.2ndWatch.image.source="https://github.com/2ndWatch/risc-python" \
    io.github.2ndWatch.image.title="RISC Client" \
    io.github.2ndWatch.image.created=$BUILD_DATETIME
