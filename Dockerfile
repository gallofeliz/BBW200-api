FROM python:3.8-alpine3.12

RUN apk add --no-cache bluez-deprecated
RUN pip install retrying

WORKDIR /app

ADD app.py .

CMD ./app.py
