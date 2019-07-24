FROM python:3.6.4
RUN mkdir /test
ADD requirements/base.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt
ADD . /test
ENV ALLOWED_HOSTS 127.0.0.1,localhost
WORKDIR /test
