FROM python:3.9-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

ENV MQTT_BROKER_ADR='localhost'
ENV MQTT_BROKER_PORT='1883'

ENV MQTT_USERNAME='user'
ENV MQTT_PASSWORD='secret'

ENV MQTT_TLS='tls_1_2'
ENV MQTT_MQTT_BROKER_CA_CERT=''


CMD ["python", "mqtt_producer.py"]