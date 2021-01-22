FROM python:alpine

RUN apk add --no-cache bluez-deprecated
RUN pip install retrying

WORKDIR /app

ADD app.py .

CMD ./app.py
