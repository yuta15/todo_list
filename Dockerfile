FROM python:3.11
COPY . /app
WORKDIR /app
RUN apt update -y && \
apt upgrade -y && \
python3 -m pip install --upgrade pip && \
python3 -m pip install -e .
