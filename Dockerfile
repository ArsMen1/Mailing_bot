FROM python:3.9.7

ENV POETRY_VERSION=1.1.11

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction

# Creating folders, and files for a project:
COPY . /code/
