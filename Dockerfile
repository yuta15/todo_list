FROM python:3.11
COPY . /app
WORKDIR /app
RUN apt update -y && \
apt upgrade -y && \
python3 -m pip install --upgrade pip && \
python3 -m pip install -e .
CMD python3 -m flask --app todo/ init-db && python3 -m flask --app todo/ run --debug --host=0.0.0.0