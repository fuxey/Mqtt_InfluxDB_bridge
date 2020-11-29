FROM python:alpine3.8

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY app/ /app
RUN ls -la /app/*

ENV MQTT_BROKER_ADR='localhost'
ENV MQTT_BROKER_PORT='1883'

ENV MQTT_USERNAME='user'
ENV MQTT_PASSWORD='secret'

ENV MQTT_TLS='tls_1_2'
ENV MQTT_MQTT_BROKER_CA_CERT=''

ENV INFLUXDB_ADR='localhost'
ENV INFLUXDB_PORT='8086'

ENV INFLUXDB_USERNAME='root'
ENV INFLUXDB_PASSWORD='root'

ENV FLASK_ENV='Production'

EXPOSE 8000
CMD python run.py --brokeradr=$MQTT_BROKER_ADR \
                         --brokerport=$MQTT_BROKER_PORT \
                         --influxdbadr=$INFLUXDB_ADR \
                         --influxdbport=$INFLUXDB_PORT \
                         --influxdbusername=$INFLUXDB_USERNAME \
                         --influxdbpassword=$INFLUXDB_PASSWORD

#CMD ["/bin/sh"]