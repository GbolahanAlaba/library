FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /library
WORKDIR /library
copy . /library/
RUN pip install -r requirements.txt