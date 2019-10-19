FROM python:3.7.5
LABEL maintainer "naweinberger@gmail.com"

WORKDIR /usr/src
ENV PYTHONPATH=/usr/src

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./smartrent_python ./smartrent_python
COPY ./tests ./tests
