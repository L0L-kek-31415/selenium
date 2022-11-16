FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app/

RUN pip install pipenv

RUN apt-get update \
    && apt-get install -yyq netcat

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system --ignore-pipfile

COPY . .
RUN chmod 777 /app/entrypoint.sh

ENTRYPOINT /app/entrypoint.sh
#ENTRYPOINT python start.py

