from influxdb import InfluxDBClient
import ssl
import logging


from influxdb.exceptions import InfluxDBClientError

logger = logging.getLogger("mqttInfluxDBPusher")


class InfluxDBConnector:
    def __init__(self):
        logger.info("create influxdb connector")
        self.dbSavingErrorCnt = 0

    def connect_to_database(self,ip, port, userName, password, dataBase):
        try:
            self.influxdbClient = InfluxDBClient(host=ip, port= port,
                                                 username= userName,
                                                 password=password,
                                                 database= dataBase)
            self.influxdbClient.create_database(dataBase)
        except InfluxDBClientError as e:
            logger.error("unable to connect to influxdb database" + e)


    def write_jsondata_in_database(self, jsonData, measurementName, hostName):
        jsonToSave = [{"measurement": measurementName, "tags": {
            "host": hostName,
            "valuetype": measurementName
        }, "fields": jsonData}]
        if not self.influxdbClient.write_points(jsonToSave, time_precision="s"):
            logger.warning("Saving Json Value in InfluxDB went wrong!")
            self.dbSavingErrorCnt += 1

    def create_database(self, databaseName):
        self.influxdbClient.create_database(databaseName)


    def list_databases(self):
        return self.influxdbClient.get_list_database()



