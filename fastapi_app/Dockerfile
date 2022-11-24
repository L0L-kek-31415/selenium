FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system --ignore-pipfile

COPY . .
