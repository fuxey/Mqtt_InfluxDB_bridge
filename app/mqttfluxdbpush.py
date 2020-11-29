import json
import logging
import threading
import time

from influxdb_client import InfluxDBConnector
from mqtt_client import MqttClient

logger = logging.getLogger("mqttInfluxDBPusher")


class mqttListener:
    def __init__(self, topic, influxInst, measurementName, hostName):
        self.topic = topic
        self.influxInst = influxInst
        self.measurementName = measurementName
        self.hostName = hostName

    def mqtt_message_to_InfluxDB(self, payload):
        logger.debug("receive message in mqtt_message_to_influxDb")
        try:
            json_data = json.loads(str(payload))
            self.influxInst.write_jsondata_in_database(json_data,
                                                       self.measurementName,
                                                       self.hostName)
        except ValueError as e:
            logger.warning("ValueError " + str(self.topic))

    def __del__(self):
        logger.info("listener for topic" + self.topic + "killed")


class mqttInfluxDBBridge(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mqtt_client = None
        self.influxdbClient = InfluxDBConnector()
        self.topicToSubscribe = []
        logger.info("create mqtt - InfluxDB - Bridge")
        self.mqttListenerDict = {}

    def run(self):
        while True:
            self.mqtt_client.mqtt_run()

    def connectToDataBase(self, ip, port, userName, password, dataBase):
        self.influxdbClient.connect_to_database(ip=ip,
                                                port=port,
                                                userName=userName,
                                                password=password,
                                                dataBase=dataBase)

    def connectToMqttBroker(self, ip, port, certspath):
        self.mqtt_client = MqttClient(ip, port)
        if certspath:
            self.mqtt_client.set_secure_connection(certspath)

        self.mqtt_client.connect_to_broker()

    def add_mqtt_topic(self, topic):
        listenerObj = mqttListener(topic=topic,
                                   influxInst=self.influxdbClient,
                                   measurementName=str(topic).replace("/", "_", 2),
                                   hostName="OrangeP")
        self.mqttListenerDict[topic] = listenerObj
        self.mqtt_client.add_listener(topic=topic, listener=listenerObj.mqtt_message_to_InfluxDB)

    def get_all_subscribed_Topics(self):
        return self.mqttListenerDict.keys()

    def remove_subscribed(self, topic):
        if topic in self.mqttListenerDict:
            self.mqtt_client.unsubscribe_topic(topic)
            # del self.mqttListenerDict[topic]
            self.mqttListenerDict.pop(topic)

    def create_database(self, name):
        self.influxdbClient.create_database(name)

    def list_database(self):
        return self.influxdbClient.list_databases()


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Input agrs for mqttInfluxdbPusher')
    # parser.add_argument("jsonpath", help="path for json input parameter", type=str)
    # args = parser.parse_args()

    # print(args.jsonpath)

    x = mqttInfluxDBBridge()
    x.connectToDataBase("localhost", 8086, "root", "root", "example1")
    x.connectToMqttBroker("localhost", 1883, "")
    x.start()
    x.add_mqtt_topic("/test")
    logger.info("get all topics:" + str(x.get_all_subscribed_Topics()))

    while True:
        logger.info("poll restinterface for possible new topics...")
        time.sleep(20)
