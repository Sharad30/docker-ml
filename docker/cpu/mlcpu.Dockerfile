FROM python:3.9.6-slim-buster
# default location for all subsequent commands
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
    numpy \
    pandas \
    pandas-profiling[notebook] \
    streamlit-pandas-profiling \
    jupyter \
    ipywidgets \
    pydantic \
    tqdm \
    click \
    loguru \
    streamlit \
    fastcore \
    matplotlib \
    seaborn \
    plotnine \
    wandb \
    data-science-types \
    scikit-learn \
    xgboost \
    lightgbm \
    # catboost \
    category-encoders \
    missingno \
    optuna 
RUN jupyter nbextension enable --py widgetsnbextension

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN pip3 freeze > requirements.txt

# COPY the code OR Receive data location from local data service
# Receive data location from local data service
