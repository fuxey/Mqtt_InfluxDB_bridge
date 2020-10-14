from flask_migrate import Migrate
from os import environ
from sys import exit
from app import create_app
from decouple import config
from config import config_dict
from mqttfluxdbpush import mqttInfluxDBBridge

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')



x =  mqttInfluxDBBridge()
x.connectToDataBase("localhost", 8086, "root", "root", "example4")
x.connectToMqttBroker("192.168.178.205", 8883, "/home/df/Documents/ca.crt")
x.start()

app = create_app(app_config, x)
Migrate(app)

if __name__ == "__main__":
    app.run()
