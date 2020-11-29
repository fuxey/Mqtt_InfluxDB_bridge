import random
import time
import paho.mqtt.client as mqtt
import ssl
import logging
import threading
import json
import os
import argparse
import websocket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class mqttClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.mqttc = mqtt.Client()
        self.mqttc.enable_logger(self.logger)
        self.logger.info("create mqtt client")
        self.mqttc.on_disconnect = self.reconnect

    def reconnect(self):
        time.sleep(5)
        self.mqttc.reconnect()

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



class websocket_mqtt_bridge():
    def __init__(self):
        self.mqttClient = mqttClient()
        websocket.enableTrace(True)

    def connectToBroker(self, brokeradr, brokerport):
        self.mqttClient.connect(brokeradr,brokerport)
        self.mqttClient.start()

    def connectWebsocket(self,url):
        self.ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()


    def on_message(self, message):
        logger.info(message)
        self.mqttClient.publish("/linuxmonitor", message)


    def on_error(ws, error):
        logger.warning(error)


    def on_close(ws):
        logger.warning("### closed ###")


    def on_open(ws):
        logger.info("ws open")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--brokeradr', type=str, required=True, help="Adress of the Broker to connect to")
    parser.add_argument('--brokerport', type=int, required=True, default=1883, help="Port of the Broker to connect to")
    args = parser.parse_args()

    x = websocket_mqtt_bridge()
    x.connectToBroker(args.brokeradr,args.brokerport)
    x.connectWebsocket("ws://localhost:4002/linuxmonitor")


    while True:
        time.sleep(1)
        num2 = random.randint(12, 32)
        #x.publish("/test", '{ "temperature":' + str(num2) + ' }')
