FROM python:3.10.2-slim

RUN pip install pytest

# Install git, required for GitPython
RUN apt-get update && apt-get install -y git

RUN useradd --create-home dimsuser
WORKDIR /home/dimsuser

USER dimsuser

COPY . /home/dimsuser/
RUN pip install -r requirements.txt

ENV GIT_PYTHON_REFRESH=quiet
