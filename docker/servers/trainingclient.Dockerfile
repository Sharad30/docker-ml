FROM python:3.9.6-slim-buster
WORKDIR /
RUN apt update && apt install -y --no-install-recommends \
    git \
    build-essential \
    apt-utils \
    python3-dev \
    python3-pip \
    python3-setuptools
RUN pip3 -q install pip --upgrade
RUN pip3 install \
    pydantic \
    fastapi 