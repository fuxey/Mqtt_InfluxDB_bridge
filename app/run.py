from sys import exit
from restapi import create_app
from decouple import config
from config import config_dict
from mqttfluxdbpush import mqttInfluxDBBridge
import logging
import os
import time
import argparse
from constants import *

logger = logging.getLogger("mqttInfluxDBPusher")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("../log.out")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


# WARNING: Don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=True)
# The configuration
# get_config_mode = 'Debug' if DEBUG else 'Production'
# get_config_mode = 'Production'

# try:

# Load the configuration using the default values
#   app_config = config_dict[get_config_mode.capitalize()]

# except KeyError:
#    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


def buildApp(brokerAdr,
             brokerPort,
             influxdbAdr,
             influxdbPort,
             influxdbUserName,
             influxdbPassword):
    mqtt_influxdb_bridge_obj = mqttInfluxDBBridge()

    time.sleep(1)

    mqtt_influxdb_bridge_obj.connectToDataBase(influxdbAdr, int(influxdbPort), influxdbUserName, influxdbPassword, "example1")
    mqtt_influxdb_bridge_obj.connectToMqttBroker(brokerAdr, int(brokerPort), "")
    mqtt_influxdb_bridge_obj.start()
    mqtt_influxdb_bridge_obj.add_mqtt_topic("/test", "test_measurement_name", "test_host_name")

    logger.info("get all topics:" + str(mqtt_influxdb_bridge_obj.get_all_subscribed_Topics()))

    app = create_app()
    app.config['SECRET_KEY'] = 'S#perS3crEt_007'
    app.config['PRODUCTION'] = False
    app.config['DEBUG'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = 3600

    app.config[MQTTINFLUXDBBRIDGE_ALLTOPICS] = mqtt_influxdb_bridge_obj.get_all_subscribed_Topics
    app.config[MQTTINFLUXDBBRIDGE_ADDTOPIC] = mqtt_influxdb_bridge_obj.add_mqtt_topic
    app.config[MQTTINFLUXDBBRIDGE_REMOVETOPIC] = mqtt_influxdb_bridge_obj.remove_subscribed
    app.config[MQTTINFLUXDBBRIDGE_CREATE_DATABASE] = mqtt_influxdb_bridge_obj.create_database
    app.config[MQTTINFLUXDBBRIDGE_LIST_DATABASE] = mqtt_influxdb_bridge_obj.list_database

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--brokeradr', type=str, required=True, help="Adress of the Broker to connect to")
    parser.add_argument('--brokerport', type=int, required=True, default=1883, help="Port of the Broker to connect to")

    parser.add_argument('--influxdbusername', type=str, required=True, help="username of influxdb to connect to")
    parser.add_argument('--influxdbpassword', type=str, required=True, help="password of the influxdb to connect to")
    parser.add_argument('--influxdbadr', type=str, required=True, help="Adress of the influxdb to connect to")
    parser.add_argument('--influxdbport', type=int, required=False, default=8086,
                        help="Adress of the influxdb to connect to")

    parser.add_argument('--apiport', type=int, required=False, default=8000, help="Port where API should listen on")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="verbose output")

    args = parser.parse_args()

    logger.debug(args.brokeradr)
    logger.debug(args.brokerport)
    logger.debug(args.influxdbadr)
    logger.debug(args.influxdbport)
    logger.debug(args.influxdbusername)
    logger.debug(args.influxdbpassword)

    app = buildApp(brokerAdr=args.brokeradr,
                   brokerPort=args.brokerport,
                   influxdbAdr=args.influxdbadr,
                   influxdbPort=args.influxdbport,
                   influxdbUserName=args.influxdbusername,
                   influxdbPassword=args.influxdbpassword)

    app.run(host='0.0.0.0', port=args.apiport)
