import json
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import ssl
import logging
import threading
import time
import argparse
import socket

from influxdb.exceptions import InfluxDBClientError

logger = logging.getLogger("mqttInfluxDBPusher")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("log.out")
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class mqttInfluxDBBridge(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mqtt_client = mqtt.Client()
        self.influxdbClient = None
        self.topicToSubscribe = []
        self.cntr = 0
        self.valueErrorCnt = 0
        self.dbSavingErrorCnt = 0
        self.disconnectFlag = False
        logger.info("create mqtt - InfluxDB - Bridge")

    def addTopic(self, topicToSubscrive):
        self.topicToSubscribe.append(topicToSubscrive)
        if(self.disconnectFlag == False):
            self.mqtt_client.subscribe(str(topicToSubscrive))
            logger.info("subscrribe to " + topicToSubscrive)

    def removeTopic(self,topicToRemove):
        self.mqtt_client.unsubscribe(topicToRemove)
        # remove topic from the list.

    def getAllSubscribedTopics(self):
        return self.topicToSubscribe

    def run(self):
        while self.valueErrorCnt < 10 and self.dbSavingErrorCnt < 10:
            self.mqtt_client.loop_forever()

    def connectToDataBase(self, ip, port, userName, password, dataBase):
        try:
            self.influxdbClient = InfluxDBClient(ip, port, userName, password, dataBase)
            self.influxdbClient.create_database(dataBase)
        except InfluxDBClientError as e:
            logger.error("unable to connect to influxdb database" + e)

    def connectToMqttBroker(self, ip, port, certspath):
        self.mqtt_client = mqtt.Client("mqttInfluxDBPusher3")
        self.mqtt_client.on_connect = self.onMqttConnection
        self.mqtt_client.on_message = self.onMqttMessage
        self.mqtt_client.on_disconnect = self.onMqttDisconnection

        try:
            self.mqtt_client.tls_set(ca_certs=certspath, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                                     tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
            self.mqtt_client.tls_insecure_set(True)
            self.mqtt_client.connect(ip, port, 10)
        except ssl.SSLError as e:
            logging.warning("uneable to connect to Broker " + str(ip))

    def onMqttDisconnection(self, client, userdata, rc):
        print("on disconnection!")
        self.disconnectFlag = True

    def onMqttConnection(self, client, userdata, flags, rc):
        logger.info("Connected successfully to MQttBroker, try to subscribe to " + str(self.topicToSubscribe))
        for elem in self.topicToSubscribe:
            self.mqtt_client.subscribe(str(elem))
            logger.info("subscrribe to " + elem)

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

    def onMqttMessage(self, client, userdata, msg):
        self.cntr += 1

        logger.debug(msg.topic + " \n " + str(msg.payload.decode()))
        try:
            json_data = json.loads(str(msg.payload.decode()))
            self.writeDataInDataBase(json_data, str(msg.topic).replace("/", "_", 2), "OrangePi")
        except ValueError as e:
            self.valueErrorCnt += 1
            logger.warning("ValueError" + e + "errocrnt " + str(self.valueErrorCnt))

    def writeDataInDataBase(self, jsonData, measurementName, hostName):
        jsonToSave = [{"measurement": measurementName, "tags": {
            "host": hostName,
            "valuetype": measurementName
        }, "fields": jsonData}]
        if self.influxdbClient.write_points(jsonToSave, time_precision="s") == False:
            logger.warning("Saving Json Value in InfluxDB went wrong!")
            self.dbSavingErrorCnt += 1


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Input agrs for mqttInfluxdbPusher')
    # parser.add_argument("jsonpath", help="path for json input parameter", type=str)
    # args = parser.parse_args()

    # print(args.jsonpath)

    list = ["/Orangepi/logging", "/Orangepi/BME680Values", "/Orangepi/system"]

    x = mqttInfluxDBBridge(list)
    x.connectToDataBase("localhost", 8086, "root", "root", "example4")
    x.connectToMqttBroker("192.168.178.205", 8883, "/home/df/Documents/ca.crt")
    x.start()

    while True:
        logger.info("poll restinterface for possible new topics...")
        time.sleep(5)