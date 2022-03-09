FROM python:3.10.2-slim

RUN pip install pipenv

RUN useradd --create-home imsuser
WORKDIR /home/imsuser
USER imsuser

COPY . /home/imsuser/
RUN pipenv install --deploy --system

CMD [ "python3", "wsgi.py" ]
