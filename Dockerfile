FROM python:3.10-alpine

WORKDIR /app

RUN apk update && apk add weasyprint msttcorefonts-installer fontconfig
RUN update-ms-fonts
RUN pip install --upgrade pip

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY ./server /app
COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
