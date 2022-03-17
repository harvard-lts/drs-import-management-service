FROM python:3.10.2-slim

RUN pip install pipenv
RUN pip install pytest

RUN useradd --create-home dimsuser
WORKDIR /home/dimsuser

USER dimsuser

COPY .. /home/dimsuser/
RUN pipenv install --deploy --system
