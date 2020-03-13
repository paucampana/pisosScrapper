FROM python:3.6-alpine3.7

RUN \
    apk update && \
    apk add ca-certificates wget && \
    update-ca-certificates && \
    apk add openssl
RUN apk add --no-cache curl

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.7/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.7/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

COPY ./app /app
RUN pip3 install -r /app/requirements.txt
WORKDIR /app/src

CMD ["python3.6", "-u", "main.py"]