FROM python:3.10.2-slim

RUN pip install pipenv

RUN groupadd -r -g 55020 dimsadm \
    && useradd -u 55020 -g 55020 --create-home dimsuser

WORKDIR /home/dimsuser
USER dimsuser

COPY . /home/dimsuser/
RUN pipenv install --deploy --system

CMD [ "python3", "wsgi.py" ]
