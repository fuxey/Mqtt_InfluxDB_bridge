import random
import time
import paho.mqtt.client as mqtt
import ssl
import logging
import threading
import json

logging.basicConfig(level=logging.DEBUG)


class mqttClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.mqttc = mqtt.Client()
        self.mqttc.enable_logger(self.logger)
        self.logger.info("create mqtt client")

    def connect(self, server, port):
        self.mqttc.connect(server, port, 60)
        self.mqttc.on_message = self.onMqttMessage

    def subscribe(self):
        self.mqttc.subscribe("$SYS/#", 0)

    def publish(self, topic, message):
        logging.debug("publish: " + str(topic) + "payload: " + str(message))
        self.mqttc.publish(topic=topic, payload=message)

    def run(self):
        self.mqttc.loop_forever()

    def onMqttMessage(self, client, userdata, msg):
        self.logger.debug(msg.topic + " \n " + str(msg.payload.decode()))


if __name__ == '__main__':

    x = mqttClient()
    x.connect("localhost", 1883)
    #x.subscribe()
    x.start()

    while True:
        time.sleep(1)
        num2 = random.randint(12, 32)
        x.publish("/test", '{ "temperature":'+str(num2)+' }')
