FROM python:3.9.23-alpine3.22

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./app.py /app.py
COPY ./templates/ /templates/

ENTRYPOINT [ "python", "/app.py" ]
