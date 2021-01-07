import paho.mqtt.client as mqtt
import logging
import ssl

logger = logging.getLogger("mqttInfluxDBPusher")


class MqttClient:
    def __init__(self, brokerAdr, brokerPort):
        logger.info("create mqtt_client")
        self.mqtt_client = mqtt.Client()
        self.disconnectedFlag = False
        self.brokerAddress = brokerAdr
        self.brokerPort = brokerPort
        self.topic_to_subscribe = []
        self.receivedMessageCounter = 0
        self.disconnectCounter = 0
        self.listenerDisct = {}

    def get_received_messages_counter(self):
        return self.receivedMessageCounter

    def set_secure_connection(self, ca_cert):
        self.mqtt_client.tls_set(ca_certs=ca_cert, certfile=None, keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2,
                                 ciphers=None, cert_reqs=ssl.CERT_REQUIRED)
        self.mqtt_client.tls_insecure_set(True)

    def add_topic_to_subscribe(self, topicToSubscribe):
        self.topic_to_subscribe.append(topicToSubscribe)

    def connect_to_broker(self):
        self.mqtt_client.on_connect = self.on_connect_to_Broker
        self.mqtt_client.on_disconnect = self.on_disconnect_from_Broker
        self.mqtt_client.on_message = self.on_message_received
        try:
            self.mqtt_client.connect(self.brokerAddress, self.brokerPort, 10)
        except ssl.SSLError as e:
            logger.warning("unable to connect to Broker" + str(self.brokerAddress))

    def subscribe_to_topic(self, topic):
        logger.debug("subscribe to Topic: " + str(topic))
        self.mqtt_client.subscribe(topic)

    def unsubscribe_topic(self, topic):
        self.mqtt_client.unsubscribe(topic)
        self.listenerDisct.pop(topic)

    def on_connect_to_Broker(self, client, userdata, flags, rc):
        logger.info("Connected successfully to MQttBroker, try to subscribe to " + str(self.topic_to_subscribe))
        for elem in self.topic_to_subscribe:
            self.subscribe_to_topic(str(elem))
            logger.info("subscrribe to " + elem)

    def on_disconnect_from_Broker(self, client, userdata, rc):
        self.disconnectCounter += 1
        logger.warning("on disconnected from Broker")
        self.disconnectedFlag = True

    def on_message_received(self, client, userdata, msg):
        self.receivedMessageCounter += 1
        logger.debug(msg.topic + " \n " + str(msg.payload.decode()))

        try:
            self.listenerDisct[msg.topic](msg.payload.decode())
        except:
            logger.warning("no listener for the topic available")

    def add_listener(self, topic, listener):
        self.listenerDisct[topic] = listener
        self.subscribe_to_topic(topic)

    def mqtt_run(self):
        self.mqtt_client.loop_forever()
