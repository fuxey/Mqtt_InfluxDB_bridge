FROM python:alpine3.8

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt


CMD ["python", "mqtt_producer.py"]