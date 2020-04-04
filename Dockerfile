FROM python:3.7-alpine

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

RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy && \
    pip3 install pandas

COPY ./app /app
RUN pip3 install -r /app/requirements.txt
WORKDIR /app/src

CMD ["python", "-u", "main.py"]
