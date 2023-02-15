FROM python:3.10-alpine

RUN apk add uchardet gcc g++ musl-dev

RUN pip install Cython
