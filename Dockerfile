FROM python:3.9.23-alpine3.22

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

RUN addgroup -S user && adduser -S user -G user

COPY ./app.py /app.py
COPY ./templates/ /templates/

USER user

ENTRYPOINT [ "python", "/app.py" ]
