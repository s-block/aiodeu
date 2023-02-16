FROM python:3.10-alpine

RUN apk add uchardet gcc g++ musl-dev cython

RUN pip install Cython
