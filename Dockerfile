FROM python:alpine

RUN apk add --no-cache bluez-deprecated

WORKDIR /app

ADD app.py .

CMD ./app.py
