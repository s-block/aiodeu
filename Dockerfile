FROM python:3.11-alpine

RUN apk add uchardet gcc g++ musl-dev libffi-dev zlib-dev --quiet
RUN apk -U upgrade libcrypto3 libssl3 --quiet

RUN pip install Cython
