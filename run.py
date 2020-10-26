from flask_migrate import Migrate
from os import environ
from sys import exit
from app import create_app
from decouple import config
from config import config_dict
from mqttfluxdbpush import mqttInfluxDBBridge
import logging


logger = logging.getLogger("mqttInfluxDBPusher")
# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


x = mqttInfluxDBBridge()
x.connectToDataBase("localhost", 8086, "root", "root", "example1")
x.connectToMqttBroker("localhost", 1883, "")
x.start()
x.add_mqtt_topic("/test")

logger.info("get all topics:" + str(x.get_all_subscribed_Topics()))

app = create_app(app_config)
app.config['MQTTINFLUXDBBRIDGE_ALLTOPICS'] = x.get_all_subscribed_Topics
app.config['MQTTINFLUXDBBRIDGE_ADDTOPIC'] = x.add_mqtt_topic
app.config['MQTTINFLUXDBBRIDGE_REMOVETOPIC'] = x.remove_subscribed



if __name__ == "__main__":
    app.run()
