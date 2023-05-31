FROM python:3.10-alpine

RUN apk add uchardet gcc g++ musl-dev --quiet
RUN apk -U upgrade libcrypto3 libssl3 --quiet

RUN pip install Cython
