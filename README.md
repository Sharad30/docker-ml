# docker-ml

## Getting Started

1. Clone the repository
2. Install asdf using this [guide](https://asdf-vm.com/#/core-manage-asdf-vm?id=install)
3. Install `python3.9.6`
```bash
asdf plugin add python
asdf install python 3.9.6
```
4. Install poetry. [Poetry](https://python-poetry.org/docs/)
```bash
asdf plugin add poetry
asdf install poetry latest
asdf local poetry 1.1.12
```
5. Install all dependencies: `poetry install`
6. Integrating commitizen with pre-commit: `poetry run pre-commit install --hook-type commit-msg`

## Build a docker container

```bash
docker-compose up --build -d
```

## Train ML model

```bash
docker-compose up
```